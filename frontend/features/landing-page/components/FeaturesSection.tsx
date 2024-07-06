import { Button } from "@common/components";
import Image from "next/image";
import React from "react";

export const FeaturesSection = () => {
  const features: SingleFeatureProps[] = [
    {
      img: {
        src: "/assets/sign-language-to-text-card.png",
        alt: "photo",
        left: true,
      },
      title: "Sign-Language-to-Text 📑",
      descriptions: [
        "Sign-Language-to-Text converts sign language to text captions as sign language appears in the video.",
        "This feature enhances accessibility for deaf TikTok creators, ensuring they can create TikTok content that is understandable by the TikTok audience. This feature also allows TikTok audience to follow the video's content more easily even if they do not know sign language.",
        "Sign-Language-to-Text can be added during video editing by selecting the video, then choosing “Sign Language to Text Caption”. Available in select countries with more to follow.",
      ],
    },
    {
      img: {
        src: "/assets/sign-language-to-speech-card.png",
        alt: "photo",
        left: false,
      },
      title: "Sign-Language-to-Speech 🔊",
      descriptions: [
        "Sign-Language-to-Speech converts sign language to a voiceover that plays over the video as the sign language appears in the video.",
        "Options for Voice-over can be customised - Gender, Language, etc.",
        "This feature enhances accessibility for deaf TikTok creators, ensuring they can create TikTok content that is understandable by the TikTok audience. This feature also allows TikTok audience to follow the video's content more easily even if they do not know sign language.",
        "Sign-Language-to-Text can be added during video editing by selecting the video, then choosing “Sign Language to Speech. Available in select countries with more to follow.",
      ],
    },
    {
      img: {
        src: "/assets/sign-language-to-emoji-card.png",
        alt: "photo",
        left: true,
      },
      title: "Sign-Language-to-Emoji 👋🏻",
      descriptions: [
        "Sign-Language-to-Emoji converts sign language to emoji text captions as the sign language appears in the video.",
        "This feature enhances accessibility for deaf TikTok creators, ensuring they can create TikTok content that is understandable by the TikTok audience. This feature also allows TikTok audience to follow the video's content more easily even if they do not know sign language.",
        "Sign-Language-to-Emoji can be added during video editing by selecting the video, then choosing “Sign Language to Emoji. Available in select countries with more to follow.",
      ],
    },
  ];

  return (
    <div className="px-6 md:px-24 flex flex-col items-center mb-12">
      <FeaturesSectionHeader />

      <div className="flex flex-col gap-16">
        {features.map((feature) => (
          <SingleFeature
            key={feature.title}
            img={{
              src: feature.img.src,
              alt: feature.img.alt,
              left: feature.img.left,
            }}
            title={feature.title}
            descriptions={feature.descriptions}
          />
        ))}
      </div>

      <Button variant="outline" className="!w-full mt-12">
        Try Now
      </Button>
    </div>
  );
};

const FeaturesSectionHeader = () => {
  return (
    <>
      <div className="font-bold text-[24px] text-tiktok-red mb-2">
        AiSL Accessibility Features
      </div>
      <div className="max-w-[750px] mb-24">
        Thank you for joining us on our journey as we make TikTok more
        accessible for all. Below are some of the features we&apos;ve launched
        with accessibility in mind.
      </div>
    </>
  );
};

interface SingleFeatureProps {
  img: {
    src: string;
    alt: string;
    left: boolean;
  };
  title: string;
  descriptions: string[];
}

const SingleFeature = (props: SingleFeatureProps) => {
  const { img, title, descriptions } = props;

  const FeatureImage = () => {
    return (
      <div className="relative h-[400px] w-full lg:w-1/2">
        <Image
          src={img.src}
          alt={img.alt}
          fill
          className="rounded-2xl object-cover"
        />
      </div>
    );
  };

  const FeatureText = () => {
    return (
      <div className="flex flex-col gap-4 w-full lg:w-1/2">
        <div className="font-bold text-[32px]">{title}</div>
        <div className="flex flex-col gap-2">
          {descriptions.map((d) => (
            <span key={d}>{d}</span>
          ))}
        </div>
        {/* <Button
          variant="outline"
          className="w-max !border-tiktok-primary !text-tiktok-primary hover:!text-white"
        >
          Try Now
        </Button> */}
      </div>
    );
  };

  return (
    <>
      {/* larger Screen */}
      <div className="hidden lg:flex flex-row items-center gap-12 w-full">
        {/* Left Image */}
        {img.left && <FeatureImage />}

        {/* Text */}
        <FeatureText />

        {/* Right Image */}
        {!img.left && <FeatureImage />}
      </div>

      {/* Smaller Screen */}
      <div className="lg:hidden flex flex-col items-center gap-6 w-full">
        {/* Image */}
        <FeatureImage />

        {/* Text */}
        <FeatureText />
      </div>
    </>
  );
};
