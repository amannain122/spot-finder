import { QRCodeSVG } from "qrcode.react";
import { Separator } from "@/components/ui/separator";

export default function SettingsProfilePage() {
  return (
    <div>
      <Separator />
      <div className="flex gap-6 justify-center flex-wrap">
        <div className="text-center flex justify-center flex-col items-center p-3 bg-gray-50 rounded-lg shadow-md mb-4 cursor-pointer">
          <QRCodeSVG
            value={"https://spot-find.vercel.app/parking?id=PL01"}
            size={140}
            bgColor={"#ffffff"}
            fgColor={"#000000"}
            level={"L"}
            includeMargin={false}
            imageSettings={{
              src: "apple-touch-icon.png",
              x: undefined,
              y: undefined,
              height: 24,
              width: 24,
              excavate: true,
            }}
          />
          <div className="mt-2">
            <h2>120 176 St, Surrey, BC V3S 9S2</h2>
          </div>
        </div>

        <div className="text-center flex justify-center flex-col items-center p-2 bg-gray-50 rounded-lg shadow-md mb-4 cursor-pointer">
          <QRCodeSVG
            value={"https://spot-find.vercel.app/parking?id=PL02"}
            size={140}
            bgColor={"#ffffff"}
            fgColor={"#000000"}
            level={"L"}
            includeMargin={false}
            imageSettings={{
              src: "apple-touch-icon.png",
              x: undefined,
              y: undefined,
              height: 24,
              width: 24,
              excavate: true,
            }}
          />
          <div className="mt-2">
            <h2>630 8 St, Canmore, AB T1W 2B5</h2>
          </div>
        </div>
        <div className="text-center flex justify-center flex-col items-center p-2 bg-gray-50 rounded-lg shadow-md mb-4 cursor-pointer">
          <QRCodeSVG
            value={"https://spot-find.vercel.app/parking?id=PL03"}
            size={140}
            bgColor={"#ffffff"}
            fgColor={"#000000"}
            level={"L"}
            includeMargin={false}
            imageSettings={{
              src: "apple-touch-icon.png",
              x: undefined,
              y: undefined,
              height: 24,
              width: 24,
              excavate: true,
            }}
          />
          <div className="mt-2">
            <h2>Main Street, East York, On</h2>
          </div>
        </div>
      </div>
    </div>
  );
}
