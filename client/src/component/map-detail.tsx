"use client";
import Map, {
  NavigationControl,
  FullscreenControl,
  ScaleControl,
  GeolocateControl,
} from "react-map-gl";

const TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN; // Set your mapbox token here

export const MapDetail = () => {
  return (
    <div className="map-detail-container rounded-sm">
      <Map
        initialViewState={{
          latitude: 43.7535611,
          longitude: -79.3323053,
          zoom: 10,
          bearing: 0,
          pitch: 0,
        }}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={TOKEN}
      >
        <GeolocateControl position="top-left" />
        <FullscreenControl position="top-left" />
        <NavigationControl position="top-left" />
        <ScaleControl />
      </Map>
    </div>
  );
};
