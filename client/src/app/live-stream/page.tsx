import { Separator } from "@/components/ui/separator";

const METADATA = [
  {
    ParkingLotID: "PL01",
    URL: "https://www.youtube.com/watch?v=HBDD3j5so0g",
    Location: "49.00426480950375, -122.73464953172447",
    "Number of Spots": 13,
    ROI: "PL01.csv",
    Address: "120 176 St, Surrey, BC V3S 9S2",
  },
  {
    ParkingLotID: "PL02",
    URL: "https://www.youtube.com/watch?v=EPKWu223XEg",
    Location: "",
    "Number of Spots": 23,
    ROI: "PL02.csv",
    Address: "",
  },
  {
    ParkingLotID: "PL03",
    URL: "https://www.youtube.com/watch?v=kC6_JqEt3GA",
    Location: "51.08961722612397, -115.35780639113904",
    "Number of Spots": 5,
    ROI: "PL03.csv",
    Address: "630 8 St, Canmore, AB T1W 2B5",
  },
];

export default function LiveStream() {
  return (
    <div>
      <Separator />
      <div className="">
        {METADATA.map((item) => (
          <div
            key={item.ParkingLotID}
            className="text-center flex justify-center flex-col items-center p-3  rounded-lg shadow-md mb-4 cursor-pointer"
          >
            {item.URL && (
              <iframe
                width="560"
                height="315"
                src={item.URL.replace("watch?v=", "embed/")}
                title="YouTube Video"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            )}
            <div className="mt-2">
              <h2>{item.Address}</h2>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
