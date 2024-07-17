<<<<<<< HEAD
 "use client";

=======
"use client";
import { Suspense } from "react";
>>>>>>> main
import { useSearchParams } from "next/navigation";
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
  const searchParams = useSearchParams();
  const search = searchParams.get("id");
  const parkingDtl: any = parkingLots?.find((data: any) => data?.id === search);

<<<<<<< HEAD
  const qrCodeUrl = `http://localhost:3000/parking-detail?id=${search}`;

=======
>>>>>>> main
  console.log(search, parkingDtl);
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div>
        <div className="flex flex-row items-center justify-between w-full px-4 gap-8 mt-8">
          {/* Add the Discover Affordable Parking Effortlessly with Spot Finder */}
          <div className=" p-4">
            <h2 className="text-lg font-semibold mb-2">{parkingDtl.address}</h2>
            <div className="flex justify-between items-center mb-2">
              <span>Availability - {parkingDtl.availability}</span>
            </div>
            <div className="mb-4">
              Rating: <span>{parkingDtl.rating.toFixed(1)}</span>
            </div>

            <br />
            <button className="bg-white text-gray-700 py-2 px-4 rounded border shadow-lg border-gray-300">
              Confirm Selection
            </button>
          </div>
<<<<<<< HEAD
          <div className="mb-4">
            Rating: <span>{parkingDtl.rating.toFixed(1)}</span>
          </div>
          <br />
          <button className="bg-white text-gray-700 py-2 px-4 rounded border shadow-lg border-gray-300">
            Confirm Selection
          </button>
        </div>

        {/* Add the Ground Floor text */}
        <div className="flex-grow">
          <img
            src={parkingDtl.image}
            alt="Parking Lot"
            className=" w-full h-full object-cover rounded-lg border-2"
            style={{ width: "500px", height: "200px" }}
          />
=======

          {/* Add the Ground Floor text */}

          <div className="">
            <img
              src={parkingDtl.image}
              alt="Parking Lot"
              className=" w-full h-full object-cover rounded-lg border-2"
            />
          </div>
>>>>>>> main
        </div>
        <MapDetail />
      </div>
<<<<<<< HEAD
      <div style={{ position: 'absolute', top: '20%', right: '18%' }}>
        <QRCodeComponent url={qrCodeUrl} />
      </div>
      <MapDetail />
    </div>
=======
    </Suspense>
>>>>>>> main
  );
};

export { ParkingDetail };
