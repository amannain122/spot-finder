import { Metadata } from "next";
import { Layout } from "@/component/layout";

export const metadata: Metadata = {
  title: "Parking QR | Spot Finder",
};

interface SettingsLayoutProps {
  children: React.ReactNode;
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
  return (
    <>
      <Layout>
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">QR Codes</h2>
          <p className="text-muted-foreground">
            Scan QR Code to book parking spot.
          </p>
        </div>
        <div className="">{children}</div>
      </Layout>
    </>
  );
}
