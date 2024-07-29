import React from "react";
import { MyBookings } from "./my-bookings";

const BookingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">My Bookings</h3>
      </div>
      <MyBookings />
    </div>
  );
};

export default BookingsPage;
