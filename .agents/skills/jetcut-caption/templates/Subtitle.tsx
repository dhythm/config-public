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
          fontWeight: 900,
          fontFamily,
          textShadow: [
            "3px 0 0 #6B21A8", "-3px 0 0 #6B21A8",
            "0 3px 0 #6B21A8", "0 -3px 0 #6B21A8",
            "3px 3px 0 #6B21A8", "-3px -3px 0 #6B21A8",
            "3px -3px 0 #6B21A8", "-3px 3px 0 #6B21A8",
            "2px 2px 4px rgba(0,0,0,0.8)",
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
