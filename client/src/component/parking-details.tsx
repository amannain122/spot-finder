"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { MapDetail } from "./map-detail";
import QRCodeComponent from "@/component/QRCodeComponent";

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
  const router = useRouter();
  const searchParams = useSearchParams();
  const search = searchParams.get("id");
  const parkingDtl: any = parkingLots.find((data: any) => data.id === search);

  const qrCodeUrl = `http://localhost:3000/parking-detail?id=${search}`;

  const handleConfirmSelection = () => {
    router.push(`/qrconfirmation?id=${search}&address=${encodeURIComponent(parkingDtl.address)}&availability=${parkingDtl.availability}&rating=${parkingDtl.rating}`);
  };

  return (
    <div>
      <div className="flex flex-row items-center justify-between w-full px-4 gap-8 mt-8">
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-2">{parkingDtl.address}</h2>
          <div className="flex justify-between items-center mb-2">
            <span>Availability - {parkingDtl.availability}</span>
          </div>
          <div className="mb-4">
            Rating: <span>{parkingDtl.rating.toFixed(1)}</span>
          </div>
          <br />
          <button
            className="bg-white text-gray-700 py-2 px-4 rounded border shadow-lg border-gray-300"
            onClick={handleConfirmSelection}
          >
            Confirm Selection
          </button>
        </div>

        <div className="flex-grow">
          <img
            src={parkingDtl.image}
            alt="Parking Lot"
            className="w-full h-full object-cover rounded-lg border-2"
            style={{ width: "500px", height: "200px" }}
          />
        </div>
      </div>
      <div style={{ position: 'absolute', top: '20%', right: '18%' }}>
        <QRCodeComponent url={qrCodeUrl} />
      </div>
      <MapDetail />
    </div>
  );
};

export { ParkingDetail };
