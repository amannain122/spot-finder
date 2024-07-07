# Parking Spot Finder Frontend

## Tech Stack

- `React` (Typescript)
- `Next.js` (local development server)
- `node.js` (version 18+ required [node.js](https://nodejs.org/en))
- `yarn/npm` (package manager)

## Run Frontend APP Locally

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

## Project Folder Structure

---

    ├── public
    ├── src
        ├── app               <- All the pages and app config
        ├── assets            <- Images, Fonts used in the project
        ├── atoms             <- reusable UI
        ├── compponent        <- Reusable components
        ├── components        <- Reusable components from shadcn UI
        ├── data              <- mock or dummy data
        ├── lib               <- Contains helper function and API connections
    ├── index.html            <- Entry Point
    ├── README.md             <- Developer Documentation
    ├── package.json          <- list of library used

---

## The project is deployed on vercel [Web App Link](https://spot-find.vercel.app)
