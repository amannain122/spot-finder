import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";

import React from "react";
import { ParkingList } from "./parking-card";

export const MapDrawer = () => {
  return (
    <div>
      <Drawer>
        <DrawerTrigger className="rounded-md border underline">
          View Parking Spots
        </DrawerTrigger>
        <DrawerContent>
          <DrawerHeader>
            <DrawerTitle>Parking Spot Listing...</DrawerTitle>
          </DrawerHeader>
          <div>
            <div className="">
              <ParkingList />
            </div>
          </div>
          <DrawerFooter>
            <DrawerClose>
              <Button variant="outline">Close</Button>
            </DrawerClose>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </div>
  );
};
