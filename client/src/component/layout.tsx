import React from "react";
import { Header } from "./header-updated";
import { Footer } from "./footer";

export const Layout = ({ children }: any) => {
  return (
    <div className="p-width m-4">
      <Header />
      <main className="relative mt-4">{children}</main>
      <Footer />
    </div>
  );
};
