import React, { useEffect } from "react";

const ParkingBox = ({ spots, onSpotClick }: any) => {
  const [filteredSpots, setFilteredSpots] = React.useState(spots);

  useEffect(() => {
    const filteredSpots = spots.filter((spot: any) => spot?.status !== "");
    setFilteredSpots(filteredSpots);
  }, [spots]);

  return (
    <div className="flex flex-wrap gap-4 justify-center">
      {filteredSpots?.map((spot: any) => (
        <div
          onClick={() => onSpotClick(spot)}
          className={`hover:shadow-lg cursor-pointer w-16 h-16 text-center flex items-center justify-center rounded-md  px-2 py-1 text-xs font-medium  ring-1 ring-inset  ${
            spot.status === "empty"
              ? "text-green-700 ring-green-600/20 bg-green-200"
              : "bg-red-50 text-red-700 ring-red-600/20"
          }`}
        >
          {spot.spot}
        </div>
      ))}
    </div>
  );
};

export { ParkingBox };
