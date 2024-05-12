FROM node:lts-alpine AS build

# Set the working directory 
WORKDIR /app

# Copy package.json and yarn.lock to the container
COPY package.json yarn.lock ./

# Install dependencies/packages
RUN yarn install --frozen-lockfile

# Copy the directory to the container
COPY . .

# Build app
RUN yarn build

FROM node:lts-alpine AS production

# Set the working directory in the container
WORKDIR /app

# Copy built files f
COPY --from=build /app/dist ./dist

RUN yarn global add serve

EXPOSE 3001

CMD ["serve", "-s", "dist", "-l", "3001"]
