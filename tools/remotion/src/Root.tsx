import React from "react";
import { Composition } from "remotion";
import { Reel } from "./Reel";
import linea from "./linea.json";

export const Root: React.FC = () => (
  <Composition
    id="a-la-medida"
    component={Reel}
    durationInFrames={linea.total}
    fps={linea.fps}
    width={1080}
    height={1920}
  />
);
