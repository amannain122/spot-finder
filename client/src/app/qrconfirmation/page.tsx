"use client";

import { useSearchParams } from "next/navigation";
import QRCodeComponent from "@/component/QRCodeComponent";
import Link from "next/link";

const QRcodeconfirmation: React.FC = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get("id");
  const address = searchParams.get("address");
  const availability = searchParams.get("availability");
  const rating = searchParams.get("rating");

  const qrCodeUrl = `http://localhost:3000/parking-detail?id=${id}`;

  return (
    <div
      style={{
        padding: "20px",
        textAlign: "center",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      {/* Added image for booking success */}
      <img
        src="https://cdn0.iconfinder.com/data/icons/df_On_Stage_Icon_Set/128/Symbol_-_Check.png"
        alt="Booking Success"
        style={{ width: "100px", height: "100px", marginBottom: "20px" }}
      />
      <h1 style={{ fontWeight: "bold", fontSize: "2em", marginBottom: "20px" }}>
        BOOKING SUCCESS!
      </h1>
      <p style={{ marginBottom: "20px" }}>
        Your parking slot is booked successfully.
      </p>
      <div
        style={{
          marginBottom: "20px",
          display: "flex",
          justifyContent: "center",
        }}
      >
        {/* Centered QR code */}
        <QRCodeComponent url={qrCodeUrl} />
      </div>
      <p style={{ marginTop: "20px", fontSize: "1.2em" }}>Location Details:</p>
      <p style={{ fontSize: "1em" }}>Address: {address}</p>
      <p style={{ fontSize: "1em" }}>Availability: {availability}</p>
      <div
        style={{
          marginTop: "40px",
          display: "flex",
          justifyContent: "center",
          gap: "20px",
        }}
      >
        <Link href="/">
          <div
            style={{
              width: "200px",
              height: "50px",
              backgroundColor: "#FFFFFF",
              borderRadius: "0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0px 4px 4px rgba(0, 0, 0, 0.25)",
            }}
          >
            <span
              style={{
                fontSize: "1em",
                fontWeight: "normal",
                color: "#000000",
              }}
            >
              Home Page
            </span>
          </div>
        </Link>
        <Link href="/booking">
          <div
            style={{
              width: "200px",
              height: "50px",
              backgroundColor: "#FFFFFF",
              borderRadius: "0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0px 4px 4px rgba(0, 0, 0, 0.25)",
            }}
          >
            <span
              style={{
                fontSize: "1em",
                fontWeight: "normal",
                color: "#000000",
              }}
            >
              Previous Bookings
            </span>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default QRcodeconfirmation;
