/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";

// interface MovingObject {
//   id: number;
//   name: string;
//   coordinates: number[];
// }

const MapComponent: React.FC = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<any>(null);
  const [lng, setLng] = useState(-79.3323053);
  const [lat, setLat] = useState(43.7535611);
  const [zoom, setZoom] = useState(9);

  useEffect(() => {
    mapboxgl.accessToken =
      "pk.eyJ1IjoicHJha2FzaHB1bjIyIiwiYSI6ImNsdzUzd3J5cjFoaTQya242YTgzcXlvZncifQ.frgsDUb2l3D8ZolT50Ab1w";

    if (mapContainer.current) {
      if (map.current) return; // initialize map only once
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: "mapbox://styles/mapbox/streets-v12",
        center: [lng, lat],
        zoom: zoom,
        maxZoom: 15,
      });

      // Add zoom controls
      map.current.addControl(new mapboxgl.NavigationControl(), "top-left");

      // Add your custom markers and lines here
      map.current.on("move", () => {
        setLng(map.current.getCenter().lng.toFixed(4));
        setLat(map.current.getCenter().lat.toFixed(4));
        setZoom(map.current.getZoom().toFixed(2));
      });

      // Clean up on unmount
    }
  }, [lat, lng, zoom]);

  return (
    <div>
      <div className="sidebar">
        Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
      </div>
      <div ref={mapContainer} style={{ height: "90vh" }} />
    </div>
  );
};

export { MapComponent };
