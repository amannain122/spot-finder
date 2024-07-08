import { ParkingList } from "@/component/parking-card";
import { MapDrawer } from "@/component/drawer";
import { SearchBox } from "@/component/search";
import { MapComponent } from "../component";
import { Header } from "@/component/header";

const Home = () => {
  return (
    <div className="p-width m-4 relative">
      <Header />
      <br />
      <SearchBox />
      <div className="flex items-center justify-center mt-4 lg:hidden">
        <MapDrawer />
      </div>
      <div className="flex mt-2">
        <div className="w-full lg:w-2/3 p-2">
          <MapComponent />
        </div>
        <div className="w-1/3 p-2 hidden lg:block flex flex-col min-h-[calc(100vh-12.5rem)] overflow-y-auto">
          <ParkingList />
        </div>
      </div>
    </div>
  );
};

export default Home;
