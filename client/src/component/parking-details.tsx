"use client";

import { useRouter, useSearchParams } from "next/navigation";
import React, { Suspense, useEffect, useState } from "react";
import { MapDetail } from "./map-detail";
import { DrawerPark } from "./parking-drawer";
import {
  confirmParkingSpot,
  getSingleParkingSpot,
  handleError,
} from "@/lib/server";
import { ParkingBox } from "./parking-box";
import { SelectSeparator } from "@/components/ui/select";
import { Loading } from "@/atoms/loading";
import { useToast } from "@/components/ui/use-toast";
import BackBtn from "@/atoms/back-btn";


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
    address: "Main Street",
    image:
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

const ParkingDetail = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const search = searchParams.get("id");
  const [parkingSpot, setParkingSpot] = useState<any>([]);
  const [loading, setLoading] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedSpot, setSelectedSpot] = useState<any>(null);
  const [time, setTime] = useState(null);
  const { toast } = useToast();

  const parking = location.find((parking) => parking.id === search);

  useEffect(() => {
    const getSpot = async () => {
      if (!search) return;
      const response = await getSingleParkingSpot(search || "PL01");
      if (response.status === "success") {
        setParkingSpot(response.data);
      }
      setLoading(false);
    };

    getSpot();
  }, []);

  const onSpotClick = (spot: any) => {
    if (spot.status === "occupied") {
      toast({ title: "This spot is already occupied" });
      return;
    }

    setSelectedSpot(spot);
    setDrawerOpen(true);
  };

  const handleDrawerClose = () => {
    setDrawerOpen(false);
    setSelectedSpot(null);
  };

  const handleConfirmSelection = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      toast({ title: "Please login first to confirm spot!!!" });
      return;
    }
    if (!selectedSpot) {
      toast({ title: "Please select a spot" });
      return;
    }
    if (!time) {
      toast({ title: "Please select time" });
      return;
    }
    if (!search) {
      toast({ title: "Invalid parking spot" });
      return;
    }

    const response = await confirmParkingSpot({
      parking_id: search,
      parking_spot: selectedSpot.spot,
      parking_time: time,
    });

    if (response.status === "success") {
      toast({ title: "Parking spot confirmed" });
      router.push(`/qrconfirmation?id=${search}`);
    } else {
      const error = handleError(response.data);
      toast({ title: error || "Failed to confirm parking spot" });
    }
  };

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div>
        <div>

          <div className="flex flex-row items-center justify-between w-full gap-8 mt-4">
            <div className="p-4">
              <BackBtn />

              <h2 className="text-lg font-semibold mb-2">
                {parking?.address || ""}
              </h2>
              <div className="flex justify-between items-center mb-4">
                Availability - {parkingSpot?.available_spots || "N/A"}
              </div>
              <DrawerPark
                open={drawerOpen}
                id={search}
                selectedSpot={selectedSpot}
                onClose={handleDrawerClose}
                time={time}
                setTime={setTime}
                onConfirm={handleConfirmSelection}
              />
              <SelectSeparator />
            </div>
          </div>
          <div className="px-4">
            <h1 className="font-medium pb-2">Parking Spots</h1>
            {loading ? (
              <div className="text-center flex justify-center">
                <Loading />
              </div>
            ) : (
              <ParkingBox
                onSpotClick={onSpotClick}
                spots={parkingSpot?.spots || []}
              />
            )}
          </div>
          <MapDetail lat={parking?.latitude} lng={parking?.longitude} />
        </div>
      </div>
    </Suspense>
  );
};

export { ParkingDetail };
