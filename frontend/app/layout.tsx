import type { Metadata } from "next";
import "@common/styles/globals.css";
import { roboto } from "@common/styles/fonts";

export const metadata: Metadata = {
  title: "TikTok AiSL",
  description: "TikTok Sign Language Accessibility for Creators and Audience!",
  icons: "./logo192.png",
  manifest: "./manifest.json",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={roboto.className}>{children}</body>
    </html>
  );
}
