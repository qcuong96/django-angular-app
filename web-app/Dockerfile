# Use an official Node runtime as the base image
FROM node:20.12.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Angular project
RUN npm run build

# Expose the port the app runs on
EXPOSE 4200

