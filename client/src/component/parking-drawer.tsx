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
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Badge } from "@/components/ui/badge";

const data = ["SP1", "SP2", "SP3", "SP4", "SP5"];

export function DrawerPark() {
  const [goal, setGoal] = React.useState(350);

  function onClick(adjustment: number) {
    setGoal(Math.max(200, Math.min(400, goal + adjustment)));
  }

  return (
    <Drawer>
      <DrawerTrigger asChild>
        <Button variant="outline">Confirm Selection</Button>
      </DrawerTrigger>
      <DrawerContent>
        <div className="mx-auto w-full max-w-sm">
          <DrawerHeader>
            <DrawerTitle>Select Spot</DrawerTitle>
            <DrawerDescription>
              Please Select Available Parking Spot.
            </DrawerDescription>
          </DrawerHeader>
          <div className="p-4 pb-0">
            {/* <div className="flex items-center justify-center space-x-2">
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8 shrink-0 rounded-full"
                onClick={() => onClick(-10)}
                disabled={goal <= 200}
              >
                <MinusIcon className="h-4 w-4" />
                <span className="sr-only">Decrease</span>
              </Button>
              <div className="flex-1 text-center">
                <div className="text-7xl font-bold tracking-tighter">
                  {goal}
                </div>
                <div className="text-[0.70rem] uppercase text-muted-foreground">
                  Calories/day
                </div>
              </div>
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8 shrink-0 rounded-full"
                onClick={() => onClick(10)}
                disabled={goal >= 400}
              >
                <PlusIcon className="h-4 w-4" />
                <span className="sr-only">Increase</span>
              </Button>
            </div> */}
            <div className="mt-3 h-[120px]">
              <ResponsiveContainer width="100%">
                <div>
                  <div className="flex gap-4">
                    {data.map((val, i) => (
                      <Badge
                        variant="outline"
                        className="cursor-pointer"
                        key={i}
                      >
                        {val}
                      </Badge>
                    ))}
                  </div>
                  <br />
                  <Select>
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
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </div>
              </ResponsiveContainer>
            </div>
          </div>
          <DrawerFooter>
            <Button>Confirm Selection</Button>
            <DrawerClose asChild>
              <Button variant="outline">Cancel</Button>
            </DrawerClose>
          </DrawerFooter>
        </div>
      </DrawerContent>
    </Drawer>
  );
}
