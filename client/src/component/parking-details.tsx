"use client";
import React, { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { MapDetail } from "./map-detail";
import { DrawerPark } from "./parking-drawer";
import { getSingleParkingSpot } from "@/lib/server";

const parkingLots = [
  {
    image: "/image1.png", // Replace with actual image URL
    address: "483 Bay street",
    distance: "900 m",
    availability: 3,
    rating: 4.2,
    id: "1",
  },
  {
    image: "/image2.png", // Replace with actual image URL
    address: "Scarborough centre station line",
    distance: "1.2 km",
    availability: 1,
    rating: 4.0,
    id: "2",
  },
  {
    image: "/image3.png", // Replace with actual image URL
    address: "Don mills station",
    distance: "1.9 km",
    availability: 2,
    rating: 4.6,
    id: "3",
  },
];

const ParkingDetail = () => {
  const searchParams = useSearchParams();
  const search = searchParams.get("id");

  const [parkingSpot, setParkingSpot] = useState<any>([]);

  useEffect(() => {
    const getSpot = async () => {
      if (!search) return;
      const response = await getSingleParkingSpot(search || "PL01");
      if (response.status === "success") {
        setParkingSpot(response.data);
      }
    };

    getSpot();
  }, []);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div>
        <div>
          <div className="flex flex-row items-center justify-between w-full px-4 gap-8 mt-8">
            {/* Add the Discover Affordable Parking Effortlessly with Spot Finder */}
            <div className=" p-4">
              <h2 className="text-lg font-semibold mb-2">
                {parkingSpot?.address || ""}
              </h2>
              <div className="flex justify-between items-center mb-2">
                <span>
                  Availability - {parkingSpot?.available_spots || "N/A"}
                </span>
              </div>
              <div className="mb-4">
                Rating: <span>{parkingSpot?.rating?.toFixed(1) || "5"}</span>
              </div>

              <br />

              <DrawerPark />
            </div>
          </div>

          <MapDetail />
        </div>
      </div>
    </Suspense>
  );
};

export { ParkingDetail };
