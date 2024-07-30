/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { useRouter } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";

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
        <h3 className="text-sm font-semibold">{address || "Main Street"}</h3>

        <p className="text-gray-600 text-sm">Availability - {availability}</p>
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

export const ParkingList = ({ parkingList, loading }: any) => {
  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center space-x-4">
          <Skeleton className="h-24 w-24 rounded" />
          <div className="space-y-2">
            <Skeleton className="h-10 w-[250px]" />
            <Skeleton className="h-4 w-[250px]" />
          </div>
        </div>
        <br />
        <div className="flex items-center space-x-4">
          <Skeleton className="h-24 w-24 rounded" />
          <div className="space-y-2">
            <Skeleton className="h-10 w-[250px]" />
            <Skeleton className="h-4 w-[250px]" />
          </div>
        </div>
        <br />
        <div className="flex items-center space-x-4">
          <Skeleton className="h-24 w-24 rounded" />
          <div className="space-y-2">
            <Skeleton className="h-10 w-[250px]" />
            <Skeleton className="h-4 w-[250px]" />
          </div>
        </div>
      </div>
    );
  }
  return (
    <div className="p-6">
      {parkingList &&
        parkingList?.map((lot: any, index: number) => (
          <ParkingLotCard
            key={index}
            image={parkingLots[index]?.image}
            address={lot.address || "Main Street"}
            distance={lot.distance}
            availability={lot.available_spots || "0"}
            rating={lot.rating || 5}
            id={lot?.parking_id || "PL01"}
          />
        ))}
    </div>
  );
};

export { ParkingLotCard };
