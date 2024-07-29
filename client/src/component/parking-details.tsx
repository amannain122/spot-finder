"use client";

import { useRouter, useSearchParams } from "next/navigation";
import QRCodeComponent from "@/component/QRCodeComponent";
import React, { Suspense, useEffect, useState } from "react";
import { MapDetail } from "./map-detail";
import { DrawerPark } from "./parking-drawer";
import { getSingleParkingSpot } from "@/lib/server";

import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { ParkingBox } from "./parking-box";
import { SelectSeparator } from "@/components/ui/select";

const location = [
  {
    id: "PL01",
    address: "120 176 St, Surrey, BC V3S 9S2, Canada",
    image:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/240px-Above_Gotham.jpg",
    state: "British Columbia",
    latitude: 49.00426480950375,
    longitude: -122.73464953172447,
  },

  {
    id: "PL02",
    city: "Main Street",
    address:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/240px-LA_Skyline_Mountains2.jpg",
    state: "Toronto",
    latitude: 43.681482424186036,
    longitude: -79.34282393314058,
  },
  {
    id: "PL03",
    address: "630 8 St, Canmore, AB T1W 2B5, Canada",
    image:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/240px-LA_Skyline_Mountains2.jpg",
    state: "Alberta",
    latitude: 51.08961722612397,
    longitude: -115.35780639113904,
  },
];

const Box = ({ position, color }: any) => (
  <mesh position={position}>
    <boxGeometry args={[1, 1, 1]} />
    <meshStandardMaterial color={color} />
  </mesh>
);

const BoxVisualization = () => {
  const boxes = [
    { position: [-2, 0.5, 0], color: "orange" },
    { position: [0, 0.5, 0], color: "orange" },
    { position: [2, 0.5, 0], color: "orange" },
    { position: [0, 0.5, -2], color: "orange" },
  ];

  return (
    <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      {boxes.map((box, index) => (
        <Box key={index} position={box.position} color={box.color} />
      ))}
      <OrbitControls />
    </Canvas>
  );
};

const ParkingDetail = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const search = searchParams.get("id");
  const [parkingSpot, setParkingSpot] = useState<any>([]);

  const parking = location.find((parking) => parking.id === search);

  console.log("sdf", parking);

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

  const handleConfirmSelection = () => {
    // router.push(`/qrconfirmation?id=${search}&address=${encodeURIComponent(parkingDtl.address)}&availability=${parkingDtl.availability}&rating=${parkingDtl.rating}`);
  };

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div>
        <div>
          <div className="flex flex-row items-center justify-between w-full gap-8 mt-8">
            <div className=" p-4">
              <h2 className="text-lg font-semibold mb-2">
                {parking?.address || ""}
              </h2>
              <div className="flex justify-between items-center mb-4">
                Availability - {parkingSpot?.available_spots || "N/A"}
              </div>
              <DrawerPark />
              <SelectSeparator />
            </div>
          </div>
          <div className="px-4">
            <h1 className="font-medium pb-2">Parking Spots</h1>
            <ParkingBox spots={parkingSpot?.spots || []} />
          </div>
          <MapDetail lat={parking?.latitude} lng={parking?.longitude} />
        </div>
      </div>
    </Suspense>
  );
};

export { ParkingDetail };
