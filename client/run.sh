#!/bin/sh

docker build -t spot-finder-app:1.0 . # buld app
docker run -d -p 3001:3001 --name spot-finder spot-finder-app:1.0