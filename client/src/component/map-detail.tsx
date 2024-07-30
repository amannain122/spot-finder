"use client";
import Map, { NavigationControl, Marker } from "react-map-gl";
import Pin from "@/atoms/pins";
const TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN; // Set your mapbox token here

export const MapDetail = ({ lat, lng }: any) => {
  return (
    <div className="map-detail-container rounded-sm">
      <Map
        initialViewState={{
          latitude: lat || 43.7535611,
          longitude: lng || -79.3323053,
          zoom: 10,
          bearing: 0,
          pitch: 0,
        }}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={TOKEN}
      >
        <NavigationControl position="top-left" />
        {lat && lng && (
          <Marker latitude={lat} longitude={lng}>
            <div style={{ color: "red", transform: "translate(-50%, -50%)" }}>
              <Pin />
            </div>
          </Marker>
        )}
      </Map>
    </div>
  );
};
