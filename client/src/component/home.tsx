"use client";
import React, { useEffect, useState } from "react";
import { getParkingSpot } from "@/lib/server";
import { ParkingList } from "./parking-card";
import { MapDrawer } from "./drawer";
import { SearchBox } from "./search";
import { MapComponent } from ".";

export const Home = () => {
  const [parkingSpot, setParkingSpot] = useState<any>([]);

  useEffect(() => {
    // get parking spot detail from the backend
    const getSpot = async () => {
      const response = await getParkingSpot();
      if (response.status === "success") {
        setParkingSpot(response.data);
      }
    };

    getSpot();
  }, []);

  return (
    <>
      <SearchBox />
      <div className="flex items-center justify-center mt-4 lg:hidden">
        <MapDrawer parkingList={parkingSpot} />
      </div>
      <div className="flex mt-2">
        <div className="w-full lg:w-2/3 p-2">
          <MapComponent />
        </div>
        <div className="w-1/3 p-2 hidden lg:block flex-col min-h-[calc(100vh-12.5rem)] overflow-y-auto">
          <ParkingList parkingList={parkingSpot} />
        </div>
      </div>
    </>
  );
};
