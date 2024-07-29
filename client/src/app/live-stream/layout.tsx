import { Metadata } from "next";
import { Layout } from "@/component/layout";

export const metadata: Metadata = {
  title: "Live Stream Link | Spot Finder",
};

interface SettingsLayoutProps {
  children: React.ReactNode;
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
  return (
    <>
      <Layout>
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">Live Stream</h2>
          <p className="text-muted-foreground">
            Youtube Live Stream that we are using for out project.
          </p>
        </div>
        <div className="">{children}</div>
      </Layout>
    </>
  );
}
