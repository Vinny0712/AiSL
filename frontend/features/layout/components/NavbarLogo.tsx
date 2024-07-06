import Image from "next/image";
import { useRouter } from "next/navigation";
import React from "react";

export const NavbarLogo = () => {
  const router = useRouter();

  return (
    <div
      className="relative w-[92px] sm:w-[130px] h-[38px] cursor-pointer"
      onClick={() => router.push("/")}
    >
      <Image src="/assets/tiktok-logo-text.svg" alt="TikTok Logo" fill />
    </div>
  );
};
