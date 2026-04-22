import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0b0b10",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          color: "white",
          fontSize: 120,
          fontWeight: 700,
          letterSpacing: -2,
          opacity,
        }}
      >
        Remotion ready
      </div>
    </AbsoluteFill>
  );
};
