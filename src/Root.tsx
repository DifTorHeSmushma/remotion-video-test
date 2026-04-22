import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld/Composition";

// Phase 4 (scene-builder) adds new composition registrations below. Keep this
// file lean — the placeholder HelloWorld composition exists only so that
// `npx remotion compositions` succeeds on a fresh checkout before any real
// video has been generated.
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
