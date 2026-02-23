# Production-optimized Dockerfile for Next.js
#
# Uses full node:22 for build stages (SWC/Turbopack needs libstdc++ and
# other system libs that node:22-slim strips out).
# Uses node:22-slim for the final production runner (minimal footprint).

# ── Base: just copy package.json ──────────────────────────────────────────────
FROM node:22 AS base
WORKDIR /app
# Only package.json — lockfile is omitted because it was generated on Windows
# and pins Windows-specific native binaries that don't exist on Linux.
COPY package.json ./

# ── Dependencies: install for Linux ───────────────────────────────────────────
FROM base AS deps
RUN npm install

# ── Builder: compile the Next.js app ──────────────────────────────────────────
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# BACKEND_URL must be available at BUILD TIME because Next.js standalone
# compiles rewrites into the server bundle during `npm run build`.
# http://backend:8000 is the internal Docker service name — always correct.
ARG BACKEND_URL=http://backend:8000
ENV BACKEND_URL=$BACKEND_URL
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# ── Runner: minimal production image ──────────────────────────────────────────
FROM node:22-slim AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
