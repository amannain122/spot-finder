import * as React from "react";
import { MinusIcon, PlusIcon } from "@radix-ui/react-icons";
import { Bar, BarChart, ResponsiveContainer } from "recharts";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";

export function DrawerPark({
  open,
  id,
  selectedSpot,
  onClose,
  time,
  setTime,
  onConfirm,
}: any) {
  return (
    <Drawer open={open}>
      <DrawerContent>
        <div className="mx-auto w-full max-w-sm">
          <DrawerHeader>
            <DrawerTitle>Confirm Spot: {id}</DrawerTitle>
            <DrawerDescription>
              Please Confirm Available Parking Spot.
            </DrawerDescription>
          </DrawerHeader>
          <div className="p-4 pb-0">
            <h2 className="text-lg font-semibold mb-2">
              Spot: {selectedSpot?.spot || ""}
            </h2>
            <div className="mt-3 h-[120px]">
              <ResponsiveContainer width="100%">
                <div>
                  <Select onValueChange={(value) => setTime(value)}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Select time" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>
                        <SelectLabel>Time</SelectLabel>
                        <SelectItem value="1">1 hour</SelectItem>
                        <SelectItem value="2">2 hours</SelectItem>
                        <SelectItem value="3">3 hours</SelectItem>
                        <SelectItem value="4">4 hours</SelectItem>
                        <SelectItem value="5">5 hours</SelectItem>
                        <SelectItem value="6">6 hours</SelectItem>
                        <SelectItem value="7">7 hours</SelectItem>
                        <SelectItem value="8">8 hours</SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </div>
              </ResponsiveContainer>
            </div>
          </div>
          <DrawerFooter>
            <Button
              onClick={onConfirm}
              aria-label="confirm selection"
              aria-live="polite"
            >
              Confirm Selection
            </Button>
            <DrawerClose asChild>
              <Button
                onClick={onClose}
                aria-label="cancel selection"
                aria-live="polite"
                variant="outline"
              >
                Cancel
              </Button>
            </DrawerClose>
          </DrawerFooter>
        </div>
      </DrawerContent>
    </Drawer>
  );
}
