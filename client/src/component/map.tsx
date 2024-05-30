"use client";
import { useState, useMemo, useCallback } from "react";
import Map, {
  Marker,
  Popup,
  NavigationControl,
  FullscreenControl,
  ScaleControl,
  GeolocateControl,
} from "react-map-gl";
import axios from "axios";
import Pin from "../atoms/pins";

import CITIES from "../data/mock-data.json";

const TOKEN =
  "pk.eyJ1IjoicHJha2FzaHB1bjIyIiwiYSI6ImNsdzUzd3J5cjFoaTQya242YTgzcXlvZncifQ.frgsDUb2l3D8ZolT50Ab1w"; // Set your mapbox token here

export const MapComponent = () => {
  const [popupInfo, setPopupInfo] = useState<any>(null);
  const [, setLng] = useState(-79.3323053);
  const [, setLat] = useState(43.7535611);
  const [, setZoom] = useState(9);
  const [pointer, setPointer] = useState<any>();

  const pins = useMemo(
    () =>
      CITIES.map((city, index) => (
        <Marker
          key={`marker-${index}`}
          longitude={city.longitude}
          latitude={city.latitude}
          anchor="bottom"
          onClick={(e) => {
            e.originalEvent.stopPropagation();
            setPopupInfo(city);
          }}
        >
          <Pin />
        </Marker>
      )),
    []
  );

  const onMarkerDrag = useCallback((event: any) => {
    setLat(event?.viewState?.latitude.toFixed(4));
    setLng(event.viewState.longitude.toFixed(4));
    setZoom(event?.viewState?.zoom?.toFixed(2));
  }, []);

  const handleClick = async (event: any) => {
    const { lngLat }: any = event;
    try {
      const response = await axios.get(
        `https://api.mapbox.com/search/geocode/v6/reverse`,
        {
          params: {
            longitude: lngLat.lng,
            latitude: lngLat.lat,
            access_token: TOKEN,
          },
        }
      );

      const placeName =
        response?.data?.features[0]?.properties?.full_address ||
        "Unknown location";
      setPointer({ lat: lngLat.lat, lng: lngLat.lng, address: placeName });
    } catch (error) {
      console.error("Error with reverse geocoding: ", error);
    }
  };

  return (
    <div className="map-container rounded-sm">
      {/* <div className="sidebar">
        Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
      </div> */}
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
        onDrag={onMarkerDrag}
        onClick={handleClick}
      >
        <GeolocateControl position="top-left" />
        <FullscreenControl position="top-left" />
        <NavigationControl position="top-left" />
        <ScaleControl />

        {pins}

        {popupInfo && (
          <Popup
            anchor="top"
            longitude={Number(popupInfo.longitude)}
            latitude={Number(popupInfo.latitude)}
            onClose={() => setPopupInfo(null)}
          >
            <div>
              {popupInfo.city}, {popupInfo.state} |{" "}
            </div>
            <img width="100%" src={popupInfo.image} />
          </Popup>
        )}
        {pointer?.address && (
          <Popup
            anchor="top"
            longitude={Number(pointer?.lng || -79.3323053)}
            latitude={Number(pointer?.lat || 43.7535611)}
            onClose={() => setPointer(null)}
          >
            <div>{pointer?.address || ""}</div>
            {/* <img
              width="100%"
              src={
                "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/240px-Above_Gotham.jpg"
              }
            /> */}
          </Popup>
        )}
      </Map>
    </div>
  );
};
