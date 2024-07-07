import { Metadata } from "next";
import { ParkingDetail } from "@/component/parking-details";
import { Separator } from "@/components/ui/separator";
import { Header } from "@/component/header";

export const metadata: Metadata = {
  title: "Select-parking | Spot Finder",
  description: "Step Project",
};

const SelectParkingPage = () => {
  return (
    <div className="p-width m-4 relative">
      <Header />
      <ParkingDetail />
      <Separator />
      {/* Add more content here as needed */}
    </div>
  );
};

export default SelectParkingPage;
