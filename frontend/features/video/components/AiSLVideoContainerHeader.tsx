import React from "react";

export const AiSLVideoContainerHeader = () => {
  return (
    <div className="flex flex-col gap-1 mb-8">
      <div className="font-bold text-[24px]">
        Upload Video <span className="text-tiktok-red">(AiSL)</span>
      </div>
      <div className="text-tiktok-gray">
        Create accessible and easily understandable sign language content with
        AiSL&apos;s AI-powered generation.
      </div>
    </div>
  );

  // Old
  // return (
  //   <div className="max-w-[500px] text-center flex flex-col gap-2 mb-8">
  //     <div className="font-bold text-tiktok-red text-[36px] md:text-[48px]">
  //       TikTok AiSL
  //     </div>
  //     <div>
  //       Create and understand accessible and inclusive content with sign
  //       language easily with&nbsp;
  //       <span className="text-tiktok-red font-bold">
  //         AiSL&apos;s AI-powered generation.
  //       </span>
  //     </div>
  //     <div>
  //       <div>1. Sign-Language-to-Text 📑</div>
  //       <div>2. Sign-Language-to-Speech 🔊</div>
  //       <div>3. Sign-Language-to-Emoji 👋🏻</div>
  //     </div>
  //   </div>
  // );
};
