import React, { useState } from "react";
import { AiSLFeatureCheckbox } from "../components";
import { Button } from "@common/components";
import { useRouter } from "next/navigation";
import customFetch from "@common/utils/customFetch";
import toast from "react-hot-toast";

interface EditAiSLContainerProps {
  uploadedVideo: File | null;
  setGeneratedVideo: React.Dispatch<React.SetStateAction<File | null>>;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const EditAiSLContainer = (props: EditAiSLContainerProps) => {
  const { uploadedVideo, setGeneratedVideo, setIsLoading } = props;

  const router = useRouter();
  const fetch = customFetch();

  const [generatedCaptions, setGeneratedCaptions] = useState("");

  const [isSignToSpeechFeatureSelected, setIsSignToSpeechFeatureSelected] =
    useState(false);
  const [isSignToEmojiFeatureSelected, setIsSignToEmojiFeatureSelected] =
    useState(false);

  const handleOnConfirmAiSLGeneration = () => {
    if (!uploadedVideo) return toast.error("Please upload a video!");

    setIsLoading(true);

    // TODO: Connect to backend
    // fetch.post("/generate", {}, "form")

    setGeneratedVideo(uploadedVideo); // TODO: Set edited video with the actual edited video
    setIsLoading(false);
    toast.success("Video Generated!");
  };

  return (
    <div>
      {/* Captions */}
      <div className="flex flex-col gap-1">
        <div className="font-bold text-[18px]">Generated Captions</div>
        <div className="text-tiktok-gray text-[14px]">
          Please check the auto-generated captions from sign language detected
          in the video (Please keep the formatting the same).
        </div>
        <textarea
          className="h-[200px] rounded-md border-2 border-gray-300 border-dashed focus:outline-none"
          value={generatedCaptions}
          onChange={(e) => {
            setGeneratedCaptions(e.target.value);
          }}
          disabled={!uploadedVideo}
        />
      </div>

      {/* Add-on AiSL Features */}
      <div className="flex flex-col gap-2 mt-4">
        <div className="font-bold">Add-on AiSL Features</div>

        <AiSLFeatureCheckbox
          label="Sign-Language-to-Speech"
          selectedDescription="A voice over based on the generated caption will be added to the video."
          isSelected={isSignToSpeechFeatureSelected}
          setIsSelected={setIsSignToSpeechFeatureSelected}
        />
        <AiSLFeatureCheckbox
          label="Sign-Language-to-Emoji"
          selectedDescription="Selecting this option will emoji-fy the generated captions."
          isSelected={isSignToEmojiFeatureSelected}
          setIsSelected={setIsSignToEmojiFeatureSelected}
        />
      </div>

      <div className="flex gap-2 mt-6">
        <Button variant="outline" onClick={() => router.push("/")}>
          Discard
        </Button>
        <Button onClick={handleOnConfirmAiSLGeneration}>Confirm</Button>
      </div>
    </div>
  );
};
