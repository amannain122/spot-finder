"use client";
import React, { useEffect } from "react";
import moment from "moment";
import { getMyBookings } from "@/lib/server";

const parkingIconUrl =
  "https://cdn1.iconfinder.com/data/icons/city-elements-56/520/416_Car_Parking_Transport-512.png";

export const MyBookings = () => {
  const [bookings, setBookings] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  console.log(bookings);

  useEffect(() => {
    const fetchBookings = async () => {
      // Fetch bookings from API
      // const response = await fetch("your-api-url");
      const response = await getMyBookings();
      if (response.status === "failure") {
        console.error(response.data);
        return;
      }

      // const data = await response.json();
      setBookings(response.data);
      setLoading(false);
    };

    fetchBookings();
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          border: "1px solid #ccc",
          marginBottom: "40px",
        }}
      >
        <thead>
          <tr>
            <th
              style={{
                border: "1px solid #ccc",
                padding: "12px",
                textAlign: "left",
              }}
            >
              Sl No
            </th>
            <th
              style={{
                border: "1px solid #ccc",
                padding: "12px",
                textAlign: "left",
              }}
            >
              Location
            </th>
            <th
              style={{
                border: "1px solid #ccc",
                padding: "12px",
                textAlign: "left",
              }}
            >
              Date
            </th>
            <th
              style={{
                border: "1px solid #ccc",
                padding: "12px",
                textAlign: "left",
              }}
            >
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={4}>Loading...</td>
            </tr>
          ) : bookings.length === 0 ? (
            <tr>
              <td colSpan={4}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    marginTop: "20px",
                  }}
                >
                  <img
                    src={parkingIconUrl}
                    alt="Parking Icon"
                    style={{ width: "180px", height: "180px" }}
                  />
                </div>
                No bookings found
              </td>
            </tr>
          ) : (
            bookings.map((booking: any, index) => (
              <tr key={booking.id || index}>
                <td
                  style={{
                    border: "1px solid #ccc",
                    padding: "12px",
                    textAlign: "left",
                  }}
                >
                  {index + 1}
                </td>
                <td
                  style={{
                    border: "1px solid #ccc",
                    padding: "12px",
                    textAlign: "left",
                  }}
                >
                  {booking?.parking_details?.address || "N/A"}
                </td>
                <td
                  style={{
                    border: "1px solid #ccc",
                    padding: "12px",
                    textAlign: "left",
                  }}
                >
                  {moment(booking?.booking_date).format(
                    "MMMM Do YYYY, h:mm:ss a"
                  ) || "N/A"}
                </td>
                <td
                  style={{
                    border: "1px solid #ccc",
                    padding: "12px",
                    textAlign: "left",
                  }}
                >
                  {booking?.booking_status || ""}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};
