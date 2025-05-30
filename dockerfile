# Use Node.js 23 Alpine as base image for smaller size
FROM node:23-alpine AS base

# Install pnpm globally
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy package manager files
COPY package.json pnpm-lock.yaml* ./
COPY .npmrc* ./

# Install all dependencies (including dev) for building
FROM base AS deps-all
RUN apk add --no-cache libc6-compat
RUN pnpm install --frozen-lockfile

# Install only production dependencies
FROM base AS deps-prod
RUN apk add --no-cache libc6-compat
RUN pnpm install --prod --frozen-lockfile

# Build stage
FROM base AS builder
COPY --from=deps-all /app/node_modules ./node_modules
COPY . .

# Copy the Docker environment file and rename it to .env.local
COPY .env.docker .env.local

# Build the application
RUN pnpm run build

# Production stage
FROM node:23-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 sveltekit

# Copy built application and production node_modules
COPY --from=builder --chown=sveltekit:nodejs /app/build ./
COPY --from=deps-prod --chown=sveltekit:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=sveltekit:nodejs /app/package.json .

# Switch to non-root user
USER sveltekit

# Expose port
EXPOSE 3000

# Set environment to production
ENV NODE_ENV=production
ENV PORT=3000

# Start the application
CMD ["node", "index.js"]