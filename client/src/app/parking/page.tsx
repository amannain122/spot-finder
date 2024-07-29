import { Metadata } from "next";
import { ParkingDetail } from "@/component/parking-details";
import { Separator } from "@/components/ui/separator";
import { Layout } from "@/component/layout";
import { Toaster } from "@/components/ui/toaster";

export const metadata: Metadata = {
  title: "Select-parking | Spot Finder",
  description: "Step Project",
};

const SelectParkingPage = () => {
  return (
    <Layout>
      <ParkingDetail />
      <Separator />
      <Toaster />
    </Layout>
  );
};

export default SelectParkingPage;
