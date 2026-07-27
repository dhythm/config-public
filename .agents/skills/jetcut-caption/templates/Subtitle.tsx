import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";

const { fontFamily } = loadFont();

interface SubtitleProps {
  lines: string[];
  fontSize: number;
}

export const Subtitle: React.FC<SubtitleProps> = ({ lines, fontSize }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 3], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      position: "absolute",
      bottom: 40,
      left: 0,
      right: 0,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      pointerEvents: "none",
      opacity,
    }}>
      {lines.map((line, i) => (
        <div key={i} style={{
          color: "#FFFFFF",
          fontSize,
          fontWeight: 500,
          fontFamily,
          textShadow: [
            "2px 0 0 #000", "-2px 0 0 #000",
            "0 2px 0 #000", "0 -2px 0 #000",
            "2px 2px 0 #000", "-2px -2px 0 #000",
            "2px -2px 0 #000", "-2px 2px 0 #000",
            "1px 1px 3px rgba(0,0,0,0.6)",
          ].join(", "),
          lineHeight: 1.4,
          whiteSpace: "nowrap",
          textAlign: "center",
        }}>
          {line}
        </div>
      ))}
    </div>
  );
};
