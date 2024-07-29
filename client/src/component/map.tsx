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

const TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN; // mapbox api token

const locationIconUrl =
  "https://cdn0.iconfinder.com/data/icons/material-design-flat/24/location-256.png";

export const MapComponent = ({
  selectedLocation,
  viewPort,
  setViewport,
}: any) => {
  const [popupInfo, setPopupInfo] = useState<any>(null);
  const [pointer, setPointer] = useState<any>();
  const [currentLocationMarker, setCurrentLocationMarker] = useState<any>(null);
  const [userLocation, setUserLocation] = useState<{
    longitude: number;
    latitude: number;
  } | null>(null);

  const pins = useMemo(
    () =>
      CITIES.map((city, index) => (
        <Marker
          key={`marker-${index}`}
          longitude={city.longitude}
          latitude={city.latitude}
          anchor="bottom"
          onClick={(e: any) => {
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
    setViewport({
      latitude: event?.viewState?.latitude || 43.7535611,
      longitude: event.viewState?.longitude || -79.3323053,
    });
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
    // Get the user's location
    showCurrentLocation();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { longitude, latitude } = position.coords;
          setUserLocation({ longitude, latitude });
        },
        (error) => {
          console.error("Error getting user location:", error);
        }
      );
    }
  }, []);

  return (
    <div className="map-container">
      <Map
        initialViewState={{
          latitude: selectedLocation?.latitude || 43.7535611,
          longitude: selectedLocation?.longitude || -79.3323053,
          zoom: 10,
          bearing: 0,
          pitch: 0,
        }}
        {...viewPort}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={TOKEN}
        onDrag={onMarkerDrag}
        onClick={handleClick}
        // onMove={setViewport}
      >
        <GeolocateControl position="top-left" />
        <FullscreenControl position="top-left" />
        <NavigationControl position="top-left" />
        <ScaleControl />

        {/* {pins} */}

        {selectedLocation?.city && (
          <Marker
            latitude={selectedLocation.latitude}
            longitude={selectedLocation.longitude}
          >
            <div style={{ color: "red", transform: "translate(-50%, -50%)" }}>
              <Pin />
            </div>
            <Popup
              latitude={selectedLocation.latitude}
              longitude={selectedLocation.longitude}
              closeButton={true}
              closeOnClick={false}
              anchor="top"
            >
              <div>
                <p>{selectedLocation.city}</p>
                <p>{selectedLocation.state}</p>
                <img
                  src={selectedLocation.image}
                  alt={selectedLocation.city}
                  style={{ width: "100px" }}
                />
              </div>
            </Popup>
          </Marker>
        )}

        {popupInfo && (
          <Popup
            anchor="top"
            longitude={Number(popupInfo.longitude)}
            latitude={Number(popupInfo.latitude)}
            onClose={() => setPopupInfo(null)}
          >
            <div className="items-center p-2 bg-gray-50 rounded-lg shadow-md mb-4">
              <h3 className="text-sm font-semibold">
                {popupInfo.city}, {popupInfo.state}
              </h3>
              <div className="m-2">
                <p className="text-gray-600 text-sm">1.2 KM</p>
                <p className="text-gray-600 text-sm">Availability - 2</p>
              </div>
              <img width="100%" src={popupInfo.image} />
            </div>
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
          </Popup>
        )}

        {/* Marker for current location */}
        {currentLocationMarker && (
          <Marker
            latitude={currentLocationMarker.latitude}
            longitude={currentLocationMarker.longitude}
            anchor="bottom"
          >
            <img
              src={locationIconUrl}
              alt="Current Location"
              style={{ width: "60px", height: "60px" }}
            />{" "}
          </Marker>
        )}
      </Map>
    </div>
  );
};
