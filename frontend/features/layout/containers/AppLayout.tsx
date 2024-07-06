"use client";

import { roboto } from "@common/styles/fonts";
import React from "react";
import { Toaster } from "react-hot-toast";
import { Navbar } from "./Navbar";

interface AppLayoutProps {
  children: React.ReactNode;
}

export const AppLayout = (props: AppLayoutProps) => {
  const { children } = props;

  return (
    <body className={"flex flex-col " + roboto.className}>
      <Toaster />

      <Navbar />

      <main>{children}</main>
    </body>
  );
};
