import Link from "next/link";
import { Metadata } from "next";
import { Separator } from "@/components/ui/separator";
import { Header } from "@/component/header";
import { ParkingTable } from "@/component/ParkingTable";

export const metadata: Metadata = {
  title: "Select-parking | Spot Finder",
  description: "Step Project",
};

const SelectParkingPage = () => {
  const tableData = [
    { location: "483 Bay street", availability: 34 },
    { location: "123 King street", availability: 12 },
    { location: "456 Queen street", availability: 5 },
    { location: "789 Dundas street", availability: 7 },
    { location: "101 Yonge street", availability: 20 },
  ];

  return (
    <div className="flex flex-col items-start min-h-screen relative">
      <Header />
      <div className="flex flex-col items-start justify-start w-full px-4 gap-8">
        {/* Add the Discover Affordable Parking Effortlessly with Spot Finder */}
        <div
          className="DiscoverAffordableParkingEffortlesslyWithSpotFinder"
          style={{ width: "100%", maxWidth: "470px", height: "231px" }}
        >
          <span
            style={{
              color: "#136F97",
              fontSize: "2.5rem",
              fontFamily: "Inter",
              fontWeight: "400",
              wordWrap: "break-word",
            }}
          >
            D
          </span>
          <span
            style={{
              color: "#136F97",
              fontSize: "2.25rem",
              fontFamily: "Inter",
              fontWeight: "400",
              wordWrap: "break-word",
            }}
          >
            iscover <br />Affordable Parking Effortlessly with <br />
          </span>
          <span
            style={{
              color: "#33B074",
              fontSize: "2.5rem",
              fontFamily: "Inter",
              fontWeight: "400",
              wordWrap: "break-word",
            }}
          >
            Spot Finder
          </span>
        </div>
        {/* Add the Group10 with BayStreet and Availability */}
        <div className="Group10 w-[214px] h-[61px] relative">
          <div className="BayStreet left-0 top-0 absolute text-black text-lg sm:text-2xl font-normal font-['Inter']">
            483 Bay street{" "}
          </div>
          <div className="Availability342 left-0 top-[37px] absolute text-black text-base sm:text-xl font-normal font-['Inter']">
            Availability - 34
          </div>
        </div>
        {/* Add the Group11 with See more details */}
        <div className="Group11 opacity-80 w-[226px] h-12 relative">
          <div className="Text left-[132px] top-[19px] absolute text-black text-lg sm:text-2xl font-normal font-['Inter']">
            {" "}
          </div>
          <div className="Rectangle9 w-[226px] h-[39px] left-0 top-0 absolute bg-cyan-700 rounded-[20px]" />
          <div className="SeeMoreDetails left-[32px] top-[7px] absolute text-white text-base sm:text-xl font-normal font-['Inter']">
            See more details
          </div>
        </div>
        {/* Add the Group9 with ConfirmSelection */}
        <div className="Group9 w-[368px] h-[76px] relative">
          <div className="Rectangle8 w-[368px] h-[76px] left-0 top-0 absolute bg-white rounded-[20px] shadow" />
          <div className="ConfirmSelection w-[261px] h-11 left-[85px] top-[22px] absolute opacity-70 text-black text-lg sm:text-2xl font-normal font-['Inter']">
            Confirm Selection
          </div>
        </div>
        {/* Add your new component Group6 */}
        <div className="w-full sm:w-96 h-96 relative">
          {/* Paste your provided JSX code here */}
        </div>
        {/* Add the Ground Floor text */}
        <div className="absolute top-[5%] left-0 sm:left-[60%] mt-4">
          <div className="text-black text-lg sm:text-2xl font-normal font-['Inter']">
            Ground Floor
          </div>
        </div>
        {/* Add the Parking Table increased size and moved slightly to the left */}
        <div className="absolute top-[20%] right-[5%] w-[80%] sm:w-[70%]">
          <ParkingTable data={tableData} />
        </div>
        {/* Add the Log Out component */}
        <div
          className="Group8 absolute top-0 right-0 mt-4"
          style={{ left: "calc(100% - 130px)" }}
        >
          <div
            className="Rectangle4"
            style={{
              width: "98px",
              height: "24px",
              left: "0",
              top: "0",
              position: "absolute",
              background: "#33B074",
              borderRadius: "35px",
            }}
          ></div>
          <div
            className="LogOut"
            style={{
              width: "91px",
              height: "24px",
              left: "24px",
              top: "0",
              position: "absolute",
              color: "#F6F9FB",
              fontSize: "0.875rem",
              fontFamily: "Inter",
              fontWeight: "400",
              wordWrap: "break-word",
            }}
          >
            Log Out
          </div>
        </div>
      </div>
      <Separator />
      {/* Add more content here as needed */}
    </div>
  );
};

export default SelectParkingPage;
