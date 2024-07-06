"use client";

import React, { useState } from "react";
import { UploadVideoContainer } from "./UploadVideoContainer";
import { AiSLVideoContainerHeader } from "../components";
import { GeneratedVideoContainer } from "./GeneratedVideoContainer";

export const AiSLVideoContainer = () => {
  const [uploadedVideo, setUploadedVideo] = useState<File | null>(null);
  const [generatedVideo, setGeneratedVideo] = useState<Blob | null>(null);

  return (
    <div className="flex flex-col px-8 py-6 m-4 sm:m-8 rounded-lg border border-tiktok-light-gray shadow">
      {/* Header */}
      <AiSLVideoContainerHeader />

      {!generatedVideo && (
        <UploadVideoContainer
          uploadedVideo={uploadedVideo}
          setUploadedVideo={setUploadedVideo}
          setGeneratedVideo={setGeneratedVideo}
        />
      )}

      {uploadedVideo && generatedVideo && (
        <GeneratedVideoContainer
          originalVideo={uploadedVideo}
          generatedVideo={generatedVideo}
        />
      )}
    </div>
  );
};
