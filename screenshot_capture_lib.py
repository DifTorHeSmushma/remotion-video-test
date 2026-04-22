"""
Core library for capturing website screenshots via agent-browser CLI.

Provides:
- run_agent_browser(): subprocess wrapper for agent-browser commands
- dismiss_obstacles(): removes cookie banners, popups, modals
- capture_screenshot(): full capture flow (navigate, wait, dismiss, capture, validate)
- validate_screenshot(): checks file exists and is non-trivial size

Used by capture-screenshots.py (batch) and can be imported for ad-hoc use.
"""

import os
import subprocess
import time
import json
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Common dismiss selectors — merged with per-entry overrides
# ---------------------------------------------------------------------------

COMMON_DISMISS_SELECTORS = [
    # Cookie banners (click)
    "#onetrust-accept-btn-handler",
    "[data-testid='cookie-banner'] button",
    ".cookie-consent button[data-action='accept']",
    ".cc-dismiss",
    "[aria-label='Accept cookies']",
    "[aria-label='Accept all']",
    "[aria-label='Accept all cookies']",
    "button.cookie-accept",
    # GitHub-specific
    ".js-cookie-consent-accept",
    "[data-action='click:signup-prompt#dismiss']",
    # Generic modals / popups (click)
    "[aria-label='Close']",
    "[aria-label='Dismiss']",
    ".modal-close",
    "button.close",
    ".popup-close",
    "[data-dismiss='modal']",
]

# Selectors to force-remove from DOM if clicking didn't work
COMMON_REMOVE_SELECTORS = [
    "#onetrust-banner-sdk",
    "#onetrust-consent-sdk",
    "[data-testid='cookie-banner']",
    ".cookie-consent",
    ".cookie-banner",
    ".cc-window",
    ".modal-backdrop",
    ".overlay-backdrop",
    # Newsletter / signup popups
    ".popup-overlay",
    "[class*='newsletter']",
    "[class*='signup-prompt']",
]

RETRY_DELAYS_S = [2, 5, 10]
MIN_SCREENSHOT_KB = 10


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CaptureResult:
    name: str
    url: str
    output_path: str
    success: bool
    file_size_kb: float = 0.0
    error: Optional[str] = None
    attempts: int = 1
    staticfile_path: str = ""


@dataclass
class ScreenshotEntry:
    """Parsed from a single entry in screenshots.json."""
    name: str
    url: str
    scene: str = ""
    usage: str = ""
    viewport: tuple = (1920, 1080)
    color_scheme: str = "dark"
    wait_strategy: str = "networkidle"
    full_page: bool = False
    scroll_to_selector: Optional[str] = None
    dismiss_selectors: list = field(default_factory=list)
    eval_before: Optional[str] = None
    wait_for_selector: Optional[str] = None
    delay_after_load_ms: int = 1500
    retries: int = 2
    skip_if_exists: bool = True

    @classmethod
    def from_dict(cls, d: dict, defaults: dict) -> "ScreenshotEntry":
        """Create from manifest dict, merging defaults."""
        vp = d.get("viewport") or defaults.get("viewport", [1920, 1080])
        if isinstance(vp, dict):
            vp = (vp.get("width", 1920), vp.get("height", 1080))
        elif isinstance(vp, list):
            vp = tuple(vp)

        return cls(
            name=d["name"],
            url=d["url"],
            scene=d.get("scene", ""),
            usage=d.get("usage", ""),
            viewport=vp,
            color_scheme=d.get("color_scheme", defaults.get("color_scheme", "dark")),
            wait_strategy=d.get("wait_strategy", defaults.get("wait_strategy", "networkidle")),
            full_page=d.get("full_page", False),
            scroll_to_selector=d.get("scroll_to_selector"),
            dismiss_selectors=d.get("dismiss_selectors", []),
            eval_before=d.get("eval_before"),
            wait_for_selector=d.get("wait_for_selector"),
            delay_after_load_ms=d.get("delay_after_load_ms", defaults.get("delay_after_load_ms", 1500)),
            retries=d.get("retries", 2),
            skip_if_exists=d.get("skip_if_exists", True),
        )


# ---------------------------------------------------------------------------
# agent-browser subprocess wrapper
# ---------------------------------------------------------------------------

def run_agent_browser(args: str, timeout_s: int = 60) -> tuple:
    """
    Run an agent-browser CLI command.

    Returns (returncode, stdout, stderr).
    """
    cmd = f"agent-browser {args}"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout after {timeout_s}s: {cmd}"
    except Exception as e:
        return -1, "", str(e)


# ---------------------------------------------------------------------------
# Obstacle dismissal
# ---------------------------------------------------------------------------

def dismiss_obstacles(extra_selectors: list = None) -> int:
    """
    Attempt to dismiss cookie banners, popups, and modals.

    Returns count of elements dismissed/removed.
    """
    dismissed = 0

    # Phase 1: Try clicking common dismiss buttons
    all_click_selectors = COMMON_DISMISS_SELECTORS + (extra_selectors or [])
    for sel in all_click_selectors:
        # Use JS click — more reliable than agent-browser click for overlay elements
        escaped = sel.replace("'", "\\'")
        js = f"(function(){{ var el = document.querySelector('{escaped}'); if(el){{ el.click(); return 'clicked'; }} return 'not_found'; }})()"
        rc, out, _ = run_agent_browser(f'eval "{js}"', timeout_s=5)
        if rc == 0 and "clicked" in out:
            dismissed += 1

    # Brief wait for DOM to settle after clicks
    if dismissed > 0:
        run_agent_browser("wait 500", timeout_s=5)

    # Phase 2: Force-remove persistent overlays from DOM
    for sel in COMMON_REMOVE_SELECTORS:
        escaped = sel.replace("'", "\\'")
        js = f"(function(){{ var el = document.querySelector('{escaped}'); if(el){{ el.remove(); return 'removed'; }} return 'not_found'; }})()"
        rc, out, _ = run_agent_browser(f'eval "{js}"', timeout_s=5)
        if rc == 0 and "removed" in out:
            dismissed += 1

    # Phase 3: Remove any fixed/sticky overlays that cover the viewport
    js_remove_overlays = """(function(){
        var removed = 0;
        document.querySelectorAll('div, aside, section').forEach(function(el){
            var s = getComputedStyle(el);
            if ((s.position === 'fixed' || s.position === 'sticky') && parseInt(s.zIndex) > 999) {
                el.remove();
                removed++;
            }
        });
        return 'removed_' + removed;
    })()"""
    rc, out, _ = run_agent_browser(f'eval "{js_remove_overlays}"', timeout_s=10)
    if rc == 0 and "removed_" in out:
        try:
            count = int(out.split("removed_")[-1])
            dismissed += count
        except ValueError:
            pass

    if dismissed > 0:
        run_agent_browser("wait 500", timeout_s=5)

    return dismissed


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_screenshot(path: str, min_kb: float = MIN_SCREENSHOT_KB) -> tuple:
    """
    Validate a captured screenshot.

    Returns (is_valid, file_size_kb, error_message).
    """
    if not os.path.isfile(path):
        return False, 0.0, "File does not exist"

    size_kb = os.path.getsize(path) / 1024.0
    if size_kb < min_kb:
        return False, size_kb, f"File too small ({size_kb:.1f}KB < {min_kb}KB) — likely blank or error page"

    return True, size_kb, None


# ---------------------------------------------------------------------------
# Main capture function
# ---------------------------------------------------------------------------

def capture_screenshot(entry: ScreenshotEntry, output_dir: str, dry_run: bool = False) -> CaptureResult:
    """
    Capture a single screenshot according to the entry spec.

    Full flow: viewport -> color scheme -> navigate -> wait -> dismiss -> eval -> scroll -> capture -> validate.
    Retries on failure with increasing delay.
    """
    output_path = os.path.join(output_dir, f"{entry.name}.png")

    # Build staticFile path (forward slashes, relative to public/)
    rel_path = output_path.replace("\\", "/")
    if "public/" in rel_path:
        staticfile = rel_path.split("public/", 1)[1]
    else:
        staticfile = rel_path

    # Skip if exists
    if entry.skip_if_exists and os.path.isfile(output_path):
        size_kb = os.path.getsize(output_path) / 1024.0
        return CaptureResult(
            name=entry.name,
            url=entry.url,
            output_path=output_path,
            success=True,
            file_size_kb=size_kb,
            error="Skipped (already exists)",
            staticfile_path=staticfile,
        )

    # Dry run — just print what would happen
    if dry_run:
        print(f"  [DRY RUN] Would capture:")
        print(f"    agent-browser set viewport {entry.viewport[0]} {entry.viewport[1]}")
        print(f"    agent-browser set media {entry.color_scheme}")
        print(f"    agent-browser open {entry.url}")
        print(f"    agent-browser wait --load {entry.wait_strategy}")
        print(f"    agent-browser wait {entry.delay_after_load_ms}")
        if entry.wait_for_selector:
            print(f"    agent-browser wait \"{entry.wait_for_selector}\"")
        print(f"    dismiss_obstacles({len(entry.dismiss_selectors)} extra selectors)")
        if entry.eval_before:
            print(f"    agent-browser eval \"{entry.eval_before[:80]}...\"")
        if entry.scroll_to_selector:
            print(f"    agent-browser scrollintoview \"{entry.scroll_to_selector}\"")
        full_flag = " --full" if entry.full_page else ""
        print(f"    agent-browser screenshot{full_flag} {output_path}")
        return CaptureResult(
            name=entry.name,
            url=entry.url,
            output_path=output_path,
            success=True,
            error="Dry run",
            staticfile_path=staticfile,
        )

    # Actual capture with retries
    max_attempts = entry.retries + 1
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            result = _attempt_capture(entry, output_path)
            if result.success:
                result.attempts = attempt
                result.staticfile_path = staticfile
                return result
            last_error = result.error
        except Exception as e:
            last_error = str(e)

        # Retry: close browser, wait, reopen
        if attempt < max_attempts:
            delay = RETRY_DELAYS_S[min(attempt - 1, len(RETRY_DELAYS_S) - 1)]
            print(f"    Retry {attempt}/{entry.retries} in {delay}s... ({last_error})")
            run_agent_browser("close", timeout_s=10)
            time.sleep(delay)

    return CaptureResult(
        name=entry.name,
        url=entry.url,
        output_path=output_path,
        success=False,
        error=last_error or "Unknown error",
        attempts=max_attempts,
        staticfile_path=staticfile,
    )


def _attempt_capture(entry: ScreenshotEntry, output_path: str) -> CaptureResult:
    """Single capture attempt (no retry logic)."""

    # 1. Set viewport
    rc, _, err = run_agent_browser(f"set viewport {entry.viewport[0]} {entry.viewport[1]}")
    if rc != 0:
        return CaptureResult(entry.name, entry.url, output_path, False, error=f"Viewport failed: {err}")

    # 2. Set color scheme
    rc, _, err = run_agent_browser(f"set media {entry.color_scheme}")
    if rc != 0:
        # Non-fatal — some sites don't support prefers-color-scheme
        pass

    # 3. Navigate
    rc, _, err = run_agent_browser(f'open "{entry.url}"', timeout_s=30)
    if rc != 0:
        return CaptureResult(entry.name, entry.url, output_path, False, error=f"Navigation failed: {err}")

    # 4. Wait for load
    rc, _, err = run_agent_browser(f"wait --load {entry.wait_strategy}", timeout_s=30)
    if rc != 0:
        # Non-fatal — try to continue even if networkidle wasn't reached
        pass

    # 5. Extra delay for animations/lazy-loading
    if entry.delay_after_load_ms > 0:
        run_agent_browser(f"wait {entry.delay_after_load_ms}", timeout_s=max(10, entry.delay_after_load_ms // 1000 + 5))

    # 6. Wait for specific selector
    if entry.wait_for_selector:
        rc, _, _ = run_agent_browser(f'wait "{entry.wait_for_selector}"', timeout_s=15)
        # Non-fatal if element doesn't appear

    # 7. Dismiss obstacles
    dismiss_obstacles(entry.dismiss_selectors)

    # 8. Execute pre-capture JS
    if entry.eval_before:
        escaped = entry.eval_before.replace('"', '\\"')
        run_agent_browser(f'eval "{escaped}"', timeout_s=10)
        run_agent_browser("wait 500", timeout_s=5)

    # 9. Scroll to element
    if entry.scroll_to_selector:
        escaped = entry.scroll_to_selector.replace('"', '\\"')
        run_agent_browser(f'scrollintoview "{escaped}"', timeout_s=10)
        run_agent_browser("wait 500", timeout_s=5)

    # 10. Capture
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    full_flag = "--full " if entry.full_page else ""
    # Use forward slashes for the path (agent-browser on Windows)
    capture_path = output_path.replace("\\", "/")
    rc, out, err = run_agent_browser(f'screenshot {full_flag}"{capture_path}"', timeout_s=30)
    if rc != 0:
        return CaptureResult(entry.name, entry.url, output_path, False, error=f"Screenshot failed: {err}")

    # 11. Validate
    is_valid, size_kb, val_error = validate_screenshot(output_path)
    if not is_valid:
        return CaptureResult(entry.name, entry.url, output_path, False, file_size_kb=size_kb, error=val_error)

    return CaptureResult(entry.name, entry.url, output_path, True, file_size_kb=size_kb)


# ---------------------------------------------------------------------------
# Browser lifecycle helpers
# ---------------------------------------------------------------------------

def open_browser_session() -> bool:
    """Ensure a browser session is available. Returns True if ready."""
    # agent-browser auto-starts on first command, but we can verify
    rc, _, _ = run_agent_browser("set viewport 1920 1080", timeout_s=15)
    return rc == 0


def close_browser_session():
    """Close the browser session."""
    run_agent_browser("close", timeout_s=10)


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------

def load_manifest(manifest_path: str) -> tuple:
    """
    Load and parse a screenshots.json manifest.

    Returns (defaults_dict, list_of_ScreenshotEntry).
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    defaults = data.get("defaults", {})
    entries = []
    for item in data.get("screenshots", []):
        entries.append(ScreenshotEntry.from_dict(item, defaults))

    return defaults, entries
