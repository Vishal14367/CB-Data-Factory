# Frontend Dockerfile
FROM node:18-slim AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Set build-time variable for Next.js
# Render will provide this during build if configured in Blueprint
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the application
RUN npm run build

# Production environment
FROM node:18-slim AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy built assets and necessary files
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.ts ./

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
