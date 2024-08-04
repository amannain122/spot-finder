import * as React from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const locations = [
  {
    city: "120 176 St, Surrey, BC V3S 9S2, Canada",
    image:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/240px-Above_Gotham.jpg",
    state: "British Columbia",
    latitude: 49.00426480950375,
    longitude: -122.73464953172447,
  },

  {
    city: "Main Street",
    image:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/240px-LA_Skyline_Mountains2.jpg",
    state: "Toronto",
    latitude: 43.681482424186036,
    longitude: -79.34282393314058,
  },
  {
    city: "630 8 St, Canmore, AB T1W 2B5, Canada",
    image:
      "http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/240px-LA_Skyline_Mountains2.jpg",
    state: "Alberta",
    latitude: 51.08961722612397,
    longitude: -115.35780639113904,
  },
];

const SearchBox = ({ setLocation, setViewport }: any) => {
  const handleSelectChange = (value: string) => {
    const selectedLocation = locations.find(
      (location) => location.city === value
    );
    if (selectedLocation) {
      setLocation(selectedLocation);
      setViewport({
        latitude: selectedLocation.latitude,
        longitude: selectedLocation.longitude,
      });
    }
  };
  return (
    <>
      <Select onValueChange={(value) => handleSelectChange(value)}>
        <SelectTrigger className="w-full py-6 px-4 text-gray-500 placeholder-gray-300 border border-transparent rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent">
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-300"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
            viewBox="0 0 16 16"
          >
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001a1 1 0 0 0-.195.195l3.85 3.85a1 1 0 0 0 1.414-1.414l-3.85-3.85a1 1 0 0 0-.195-.195zm-5.742 1a5 5 0 1 1 0-10 5 5 0 0 1 0 10z" />
          </svg>
          <SelectValue placeholder="Select location" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Locations</SelectLabel>
            {locations.map((location, index) => (
              <SelectItem key={index} value={location.city}>
                {location.city}
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
    </>
  );
};

export { SearchBox };
