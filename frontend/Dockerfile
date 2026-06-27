# frontend/Dockerfile
# Stage 1: Build the React application
FROM node:18-alpine AS build

WORKDIR /app

# Copy lock files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy code and build application
COPY . .
RUN npm run build

# Stage 2: Serve static files with Nginx
FROM nginx:stable-alpine

# Copy custom nginx config for single page application routing (fallback to index.html)
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
