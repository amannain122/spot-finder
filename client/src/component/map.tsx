/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useMemo, useCallback } from "react";
import Map, {
  Marker,
  Popup,
  NavigationControl,
  FullscreenControl,
  ScaleControl,
  GeolocateControl,
} from "react-map-gl";
import Pin from "../atoms/pins";

import CITIES from "../data/mock-data.json";

const TOKEN =
  "pk.eyJ1IjoicHJha2FzaHB1bjIyIiwiYSI6ImNsdzUzd3J5cjFoaTQya242YTgzcXlvZncifQ.frgsDUb2l3D8ZolT50Ab1w"; // Set your mapbox token here

export const MapComponent = () => {
  const [popupInfo, setPopupInfo] = useState<any>(null);
  const [lng, setLng] = useState(-79.3323053);
  const [lat, setLat] = useState(43.7535611);
  const [zoom, setZoom] = useState(9);

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
      </Map>
    </div>
  );
};
