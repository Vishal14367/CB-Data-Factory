# Production-optimized Dockerfile for Next.js
FROM node:22-slim AS base
WORKDIR /app
# Only copy package.json — NOT package-lock.json.
# The lockfile was generated on Windows and locks in Windows-specific
# native binaries (e.g. @next/swc-win32). Omitting it forces npm to
# resolve the correct Linux binaries for this build environment.
COPY package.json ./

# Dependencies stage
FROM base AS deps
RUN npm install

# Builder stage
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build environment variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Build the application (lint + type-check disabled in next.config.ts)
RUN npm run build

# Production stage
FROM node:22-slim AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create system user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
