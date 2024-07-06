import type { Metadata } from "next";
import "@common/styles/globals.css";
import { AppLayout } from "@features/layout/containers";

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
      <AppLayout>{children}</AppLayout>
    </html>
  );
}
