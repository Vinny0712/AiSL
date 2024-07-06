"use client";

import { Button } from "@common/components";
import Image from "next/image";
import Link from "next/link";
import React from "react";
import { FaArrowDown } from "react-icons/fa6";

export const Hero = () => {
  return (
    <section className="h-[calc(100vh-71px)] flex justify-center items-center">
      <div className="flex gap-8 justify-between items-center px-8 sm:px-12 md:px-16 lg:px-24 transition-all">
        <HeroDescription />
        <HeroImage />
        <HeroNavArrow />
      </div>
    </section>
  );
};

const HeroDescription = () => {
  return (
    <div className="flex flex-col">
      <HeroDescriptionSubtitle />
      <HeroDescriptionTitle />
      <HeroDescriptionCTA />
    </div>
  );
};

const HeroDescriptionSubtitle = () => {
  return (
    <div className="flex items-center gap-2">
      <hr className="w-[40px] sm:w-[75px] border-tiktok-red border-[2px]" />
      <span className="font-semibold text-[16px] sm:text-[20px]">
        <span className="text-tiktok-red">TikTok AiSL</span>
      </span>
    </div>
  );
};

const HeroDescriptionTitle = () => {
  return (
    <div className="flex flex-col font-black text-[36px] sm:text-[42px] lg:text-[48px] mt-4">
      <span className="text-tiktok-red">Sign Language Accessibility</span>
      <span className="-translate-y-0 sm:-translate-y-2">
        for <span className="">TikTok</span> Creators and Audience
      </span>
    </div>
  );
};

const HeroDescriptionCTA = () => {
  return (
    <div className="flex flex-col gap-6 mt-4">
      <div className="text-[18px] sm:text-[20px]">
        Create and understand accessible and inclusive content with sign
        language easily with&nbsp;
        <Link
          href="/"
          className="font-bold text-tiktok-red underline underline-offset-2 cursor-pointer"
        >
          AiSL&apos;s AI-powered
        </Link>
        &nbsp;generation. Inspiring creativity and joy for all!
      </div>

      <Button className="w-max">
        <Link href="/upload">Try Now</Link>
      </Button>
    </div>
  );
};

const HeroImage = () => {
  return (
    <Image
      src="/logo512.png"
      alt="hero image"
      width={362}
      height={394}
      className="-translate-y-12 hidden lg:block"
    />
  );
};

const HeroNavArrow = () => {
  return (
    <div className="absolute bottom-12 left-1/2 -translate-x-1/2">
      <FaArrowDown
        className="w-6 h-6 text-tiktok-primary cursor-pointer animate-pulse hover:animate-none hover:scale-125 transition-all"
        onClick={() => {
          window.scrollTo({
            top: window.innerHeight - 70,
            left: 0,
            behavior: "smooth",
          });
        }}
      />
    </div>
  );
};
