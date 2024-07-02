/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { useRouter } from "next/navigation";

const ParkingLotCard = ({
  image,
  address,
  distance,
  availability,
  rating,
  id,
}: any) => {
  const router = useRouter();
 

  return (
    <div
      onClick={() => router.push(`/parking?id=${id}`)}
      className="flex items-center p-2 bg-gray-50 rounded-lg shadow-md mb-4 cursor-pointer"
    >
      <img
        src={image}
        alt="Parking Lot"
        className="w-24 h-24 object-cover rounded-lg border-2"
      />
      <div className="ml-4">
        <h3 className="text-sm font-semibold">{address}</h3>
        <p className="text-gray-600 text-sm">{distance}</p>
        <p className="text-gray-600 text-sm">Availability - {availability}</p>
      </div>
      <div className="ml-auto flex items-center">
        <p className="text-sm font-semibold">{rating}</p>
        <svg
          className="w-6 h-6 text-yellow-500 ml-1"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.518 4.674h4.905c.97 0 1.372 1.24.588 1.81l-3.97 2.884 1.518 4.674c.3.921-.755 1.688-1.54 1.177L10 13.347l-3.97 2.884c-.785.51-1.84-.256-1.54-1.177l1.518-4.674-3.97-2.884c-.784-.57-.382-1.81.588-1.81h4.905l1.518-4.674z" />
        </svg>
      </div>
    </div>
  );
};

const parkingLots = [
  {
    image: "/image1.png", // Replace with actual image URL
    address: "483 Bay street",
    distance: "900 m",
    availability: 3,
    rating: 4.2,
    id: 1,
  },
  {
    image: "/image2.png", // Replace with actual image URL
    address: "Scarborough centre station line",
    distance: "1.2 km",
    availability: 1,
    rating: 4.0,
    id: 2,
  },
  {
    image: "/image3.png", // Replace with actual image URL
    address: "Don mills station",
    distance: "1.9 km",
    availability: 2,
    rating: 4.6,
    id: 3,
  },
];

export const ParkingList = () => {
  return (
    <div className="min-h-screen p-6">
      {parkingLots.map((lot, index) => (
        <ParkingLotCard
          key={index}
          image={lot.image}
          address={lot.address}
          distance={lot.distance}
          availability={lot.availability}
          rating={lot.rating}
          id={lot.id}
        />
      ))}
    </div>
  );
};

export { ParkingLotCard };