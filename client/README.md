# Spot Finder Frontend

## Tech Stack

- `React` (Typescript)
- `Vite` (local development server)
- `node.js` (version 18+ required [node.js](https://nodejs.org/en))
- `yarn/npm` (package manager)

## Run Frontend

```bash
> yarn install # install packages
> yarn dev # run the app
```

## Run Via Docker

```bash
> bash run.sh # or
> docker build -t spot-finder-app:1.0 . # buld app
> docker image ls # list images
> docker run -d -p 3001:3001 --name spot-finder spot-finder-app:1.0
> docker image prune -a --filter "until=24h" -f # clear images
```
