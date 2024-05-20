import { SearchBox } from "@/component/search";
import { MapComponent } from "../component";
import { ParkingList } from "@/component/parking-card";
import { Header } from "@/component/header";

const Home = () => {
  return (
    <div className="p-width m-4 relative">
      <Header />
      <SearchBox />
      <div className="min-h-screen flex">
        <div className="w-2/3 p-2">
          <MapComponent />
        </div>
        <div className="w-1/3 p-2 flex flex-col min-h-[calc(100vh-6.5rem)] overflow-y-auto">
          <ParkingList />
        </div>
      </div>
    </div>
  );
};

export { Home };
