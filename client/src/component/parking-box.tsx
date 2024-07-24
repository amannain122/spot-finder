import React, { useEffect } from "react";
import { Card } from "@/components/ui/card";

const ParkingBox = ({ spots }: any) => {
  const [filteredSpots, setFilteredSpots] = React.useState(spots);

  useEffect(() => {
    const filteredSpots = spots.filter((spot: any) => spot?.status !== "");
    setFilteredSpots(filteredSpots);
  }, [spots]);
  console.log(filteredSpots);
  return (
    <div className="flex flex-wrap justify-center">
      {filteredSpots?.map((spot: any) => (
        <Card
          key={spot.spot}
          className={`w-16 h-16 m-2 text-gray-200  text-center flex items-center justify-center rounded-lg cursor-pointer ${
            spot.status === "empty" ? "bg-green-500" : "bg-red-500"
          }`}
        >
          {spot.spot}
        </Card>
      ))}
    </div>
  );
};

export { ParkingBox };
