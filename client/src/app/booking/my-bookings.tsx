"use client";
import React, { useEffect, useState } from "react";
import moment from "moment";
import { getMyBookings } from "@/lib/server";

const parkingIconUrl =
  "https://cdn1.iconfinder.com/data/icons/city-elements-56/520/416_Car_Parking_Transport-512.png";

export const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelBookingId, setCancelBookingId] = useState<number | null>(null);

  console.log(bookings);

  useEffect(() => {
    const fetchBookings = async () => {
      const response = await getMyBookings();
      if (response.status === "failure") {
        console.error(response.data);
        return;
      }
      setBookings(response.data);
      setLoading(false);
    };

    fetchBookings();
  }, []);

  const handleCancelClick = (id: number) => {
    setCancelBookingId(id);
  };

  const handleConfirmCancel = async () => {
    if (cancelBookingId !== null) {
      try {
        // Call backend API to cancel the booking
        const token = localStorage.getItem("token");
        await fetch(`http://127.0.0.1:8000/api/bookings/${cancelBookingId}/cancel/`, {
          method: "PATCH",
          headers: {
            Authorization: `JWT ${token}`,
          },
        });

        // Update the bookings state to remove the cancelled booking
        setBookings(bookings.filter((booking:any) => booking.id !== cancelBookingId));
      } catch (error) {
        console.error("Failed to cancel booking", error);
      } finally {
        setCancelBookingId(null);
      }
    }
  };

  const handleCancelDialogClose = () => {
    setCancelBookingId(null);
  };

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
            <th
              style={{
                border: "1px solid #ccc",
                padding: "12px",
                textAlign: "left",
              }}
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={5}>Loading...</td>
            </tr>
          ) : bookings.length === 0 ? (
            <tr>
              <td colSpan={5}>
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
                <td
                  style={{
                    border: "1px solid #ccc",
                    padding: "12px",
                    textAlign: "left",
                  }}
                >
                  <button
                    className={`bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ${
                      booking.booking_status === "cancelled"
                        ? "cursor-not-allowed opacity-50"
                        : ""
                    }`}
                    onClick={() => handleCancelClick(booking.id)}
                    disabled={booking.booking_status === "cancelled"}
                  >
                    Cancel
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {cancelBookingId !== null && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded shadow-md">
            <p>Do you want to cancel?</p>
            <div className="flex justify-end space-x-4 mt-4">
              <button
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                onClick={handleCancelDialogClose}
              >
                No
              </button>
              <button
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                onClick={handleConfirmCancel}
              >
                Yes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
