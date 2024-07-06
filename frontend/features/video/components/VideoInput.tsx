"use client";

import customFetch from "@common/utils/customFetch";
import React, { useState, useRef } from "react";
import toast from "react-hot-toast";
import { MdCloudUpload } from "react-icons/md";

interface VideoInputProps {
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  uploadedVideo: File | null;
  setUploadedVideo: React.Dispatch<React.SetStateAction<File | null>>;
}

export const VideoInput = (props: VideoInputProps) => {
  const { setIsLoading, uploadedVideo, setUploadedVideo } = props;

  const fetch = customFetch();
  const acceptedfileTypes = ["video/mp4", "video/mpeg"];

  const [errorMessage, setErrorMessage] = useState("");

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleFileChange = async (event: any) => {
    event.preventDefault();
    const selectedFile = event.target.files && event.target.files[0];

    if (!selectedFile)
      return setErrorMessage("Please select a video file (.mp4)!");

    if (!acceptedfileTypes.includes(selectedFile.type)) {
      toast.error("File format not accepted!");
      setErrorMessage("Please upload valid video format (.mp4)!");
      return;
    }

    setIsLoading(true);

    // Call the API to upload the video
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // TODO: Link to Backend
      // const response = await fetch.post("/upload", formData, "form");
      // console.log("File uploaded successfully:", response);
      toast.success("Video uploaded successfully!");

      setUploadedVideo(selectedFile);
    } catch (error) {
      console.error("Error uploading file:", error);
      toast.error("Failed to upload video!");

      setUploadedVideo(null);
    }

    setIsLoading(false);
  };

  return (
    <div className="flex flex-col justify-center items-center w-full sm:w-max rounded-md transition border-2 border-gray-300 border-dashed hover:border-tiktok-red focus:outline-none appearance-none cursor-pointer my-[10px] px-6 py-8">
      <label className="cursor-pointer">
        <div className="flex flex-col items-center text-center">
          <MdCloudUpload className="text-tiktok-gray h-[36px] w-[36px]" />
          <div className="font-bold mt-2">Select video to upload</div>
          <div className="flex flex-col gap-1 items-center text-tiktok-gray text-[14px] mt-4">
            <span>MP4</span>
            <span>720x1280 resolution or higher</span>
            <span>Up to 5 minutes</span>
            <span>Less than 2GB</span>
          </div>
        </div>
        <input
          type="file"
          ref={fileInputRef}
          name="file_upload"
          className="hidden"
          onChange={(event) => {
            event.persist();
            handleFileChange(event);
          }}
        />
      </label>

      {/* Error Message */}
      {uploadedVideo && (
        <div className="mt-4 text-[14px] text-tiktok-red max-w-[180px] text-center">
          File: {uploadedVideo.name}
        </div>
      )}

      {/* Error Message */}
      {errorMessage && (
        <div className="mt-4 text-[14px] text-tiktok-red font-bold max-w-[180px] text-center">
          {errorMessage}
        </div>
      )}
    </div>
  );
};
