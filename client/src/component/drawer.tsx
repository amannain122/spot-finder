import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";

import React from "react";
import { ParkingList } from "./parking-card";

export const MapDrawer = ({ parkingList }: any) => {
  return (
    <div>
      <Drawer>
        <DrawerTrigger className="rounded-md border underline">
          <span className="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-[0.9rem] font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
            View Parking Spots
          </span>
        </DrawerTrigger>
        <DrawerContent>
          <DrawerHeader>
            <DrawerTitle>Parking Spot Listing...</DrawerTitle>
          </DrawerHeader>
          <div>
            <div className="">
              <ParkingList parkingList={parkingList} />
            </div>
          </div>
          <DrawerFooter>
            <DrawerClose>
              <Button aria-label="Close" aria-live="polite" variant="outline">
                Close
              </Button>
            </DrawerClose>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </div>
  );
};
