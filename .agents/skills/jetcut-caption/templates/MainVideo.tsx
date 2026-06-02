import React from "react";
import { AbsoluteFill, Sequence, Audio, OffthreadVideo, staticFile } from "remotion";
import { Subtitle } from "./Subtitle";

const subtitles = require("../public/subtitles.json");

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Audio src={staticFile("voice_audio.wav")} volume={1} />
      <OffthreadVideo
        src={staticFile("cut_video.mp4")}
        style={{ width: "100%", height: "100%", objectFit: "contain" }}
        muted
      />
      {subtitles.map((sub: any, idx: number) => {
        const from = Math.round(sub.start * 30);
        const dur = Math.max(1, Math.round((sub.end - sub.start) * 30));
        return (
          <Sequence key={idx} from={from} durationInFrames={dur}>
            <Subtitle lines={sub.lines} fontSize={sub.fontSize} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
