import { Metadata } from "next";
import Image from "next/image";
import { Separator } from "@/components/ui/separator";
import { Header } from "@/component/header";
import { SidebarNav } from "./nav";

export const metadata: Metadata = {
  title: "Live Stream Link | Spot Finder",
};

interface SettingsLayoutProps {
  children: React.ReactNode;
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
  return (
    <>
      <div className="p-width m-4 space-y-6  pb-16 md:block">
        <Header />
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">Live Stream</h2>
          <p className="text-muted-foreground">
            Youtube Live Stream that we are using for out project.
          </p>
        </div>
        <div className="">{children}</div>
      </div>
    </>
  );
}
