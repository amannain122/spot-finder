# Task: Research about frontend and how to do a map integrating with Python

## Tech Stack for Frontend (web app)

- React.js (frontend javascript library)
- HTML & CSS

## Working with map

- Mapbox (<https://www.mapbox.com/>)
  - preferred but need to discuss (pay as you go model).
  - UI and developer friendly
- Google Maps
- Leaflet.js (<https://leafletjs.com/>)
  - Can be used but some limitation on free api
- Three.js (<https://threejs.org/>) library if we are working with 3D modeling.

## Communication between Backend

- API (Django Rest Framework - recommended)
- Since the project we are working on is going to be real time.
  - So probably WebSocket (django-channels library if we use Django for backend) for real time data (<https://channels.readthedocs.io/en/latest/>)
  - or Long Polling (<https://javascript.info/long-polling>).
- We need to work with latitude and longitude, coordinates, polygons and routing for the location.
