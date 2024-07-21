"use client";
import { useState, useMemo, useCallback, useEffect } from "react";
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

const locationIconUrl = "https://cdn0.iconfinder.com/data/icons/material-design-flat/24/location-256.png";

export const MapComponent = () => {
  const [popupInfo, setPopupInfo] = useState<any>(null);
  const [pointer, setPointer] = useState<any>();
  const [currentLocationMarker, setCurrentLocationMarker] = useState<any>(null);

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
    // Handle marker drag events if needed
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

  const showCurrentLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        console.log("Current location:", { latitude, longitude }); // Debugging line
        setCurrentLocationMarker({
          latitude,
          longitude,
        });
      },
      (error) => {
        console.error("Error getting location:", error);
      }
    );
  };

  useEffect(() => {
    showCurrentLocation();
  }, []);

  return (
    <div className="map-container" style={{ width: "100%", height: "100%" }}>
      <Map
        initialViewState={{
          latitude: 43.7535611,
          longitude: -79.3323053,
          zoom: 10,
          bearing: 0,
          pitch: 0,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={TOKEN}
        onDrag={onMarkerDrag}
        onClick={handleClick}
      >
        {/* Geolocate control */}
        <GeolocateControl position="top-left" />

        {/* Other controls */}
        <FullscreenControl position="top-left" />
        <NavigationControl position="top-left" />
        <ScaleControl />

        {/* Render markers */}
        {pins}

        {/* Popup for city information */}
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
            <img width="100%" src={popupInfo.image} alt={popupInfo.city} />
          </Popup>
        )}

        {/* Popup for pointer location */}
        {pointer?.address && (
          <Popup
            anchor="top"
            longitude={Number(pointer?.lng || -79.3323053)}
            latitude={Number(pointer?.lat || 43.7535611)}
            onClose={() => setPointer(null)}
          >
            <div>{pointer?.address || ""}</div>
          </Popup>
        )}

        {/* Marker for current location */}
        {currentLocationMarker && (
          <Marker
            latitude={currentLocationMarker.latitude}
            longitude={currentLocationMarker.longitude}
            anchor="bottom"
          >
            <img src={locationIconUrl} alt="Current Location" style={{ width: "60px", height: "60px" }} /> {/* Edited line */}
          </Marker>
        )}
      </Map>
    </div>
  );
};
