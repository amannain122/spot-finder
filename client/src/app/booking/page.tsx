import React from "react";
import { Separator } from "@/components/ui/separator";
import { Layout } from "@/component/layout";
import { MyBookings } from "./my-bookings";

const BookingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">My Bookings</h3>
      </div>
      <Separator />
      <MyBookings />
    </div>
  );
};

export default BookingsPage;
