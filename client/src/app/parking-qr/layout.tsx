import { Metadata } from "next";
import Image from "next/image";
import { Separator } from "@/components/ui/separator";
import { Header } from "@/component/header";
import { SidebarNav } from "./nav";

export const metadata: Metadata = {
  title: "Profile | Spot Finder",
};

const sidebarNavItems = [
  {
    title: "Profile",
    href: "/profile",
  },
  {
    title: "Bookings",
    href: "/",
  },
];

interface SettingsLayoutProps {
  children: React.ReactNode;
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
  return (
    <>
      <div className="p-width m-4 space-y-6  pb-16 md:block">
        <Header />
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">QR Codes</h2>
          <p className="text-muted-foreground">
            Scan QR Code to book parking spot.
          </p>
        </div>
        <div className="">{children}</div>
      </div>
    </>
  );
}
