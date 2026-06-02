import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MainVideo"
      component={MainVideo}
      durationInFrames={/* カット済み動画の秒数 × 30 */}
      fps={30}
      width={/* ffprobeで取得したwidth */}
      height={/* ffprobeで取得したheight */}
    />
  );
};
