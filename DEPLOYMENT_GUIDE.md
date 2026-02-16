# Render Deployment Guide

## Current Status
- ✅ Backend Dockerfile: Fixed and tested
- ✅ Frontend Dockerfile: Fixed and tested  
- ✅ render.yaml: Paths corrected
- ✅ .dockerignore: Added for both services
- ✅ Dependencies: All pinned to stable versions

## The Problem

Render Blueprint deployments are failing because of a configuration issue. The `render.yaml` file has been fixed, but Render might be caching the old configuration.

## Solution: Manual Service Creation

Instead of using the Blueprint, create services manually:

### Step 1: Create Backend Service

1. Go to Render Dashboard → **New** → **Web Service**
2. Connect your GitHub repo: `Vishal14367/CB-Data-Factory`
3. Configure:
   - **Name**: `cb-data-factory-backend`
   - **Region**: Singapore
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Dockerfile Path**: `Dockerfile` (relative to root directory)
   - **Docker Build Context**: `.` (current directory)
   - **Instance Type**: Free

4. **Environment Variables**:
   ```
   GROQ_API_KEY=<your-groq-api-key>
   HOST=0.0.0.0
   PORT=10000
   ```

5. Click **Create Web Service**

### Step 2: Create Frontend Service

1. Go to Render Dashboard → **New** → **Web Service**
2. Connect same repo: `Vishal14367/CB-Data-Factory`
3. Configure:
   - **Name**: `cb-data-factory-frontend`
   - **Region**: Singapore
   - **Branch**: `main`
   - **Root Directory**: `frontend_new`
   - **Runtime**: Docker
   - **Dockerfile Path**: `Dockerfile`
   - **Docker Build Context**: `.`
   - **Instance Type**: Free

4. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://cb-data-factory-backend.onrender.com
   ```
   *(Replace with your actual backend URL after Step 1)*

5. Click **Create Web Service**

## Alternative: Fix Blueprint Deployment

If you want to use the Blueprint:

1. **Delete existing Blueprint** from Render Dashboard
2. Go to **Blueprints** → **New Blueprint Instance**
3. Connect repo: `Vishal14367/CB-Data-Factory`
4. Render will read the `render.yaml` file
5. **Manually enter** `GROQ_API_KEY` when prompted
6. Deploy

## Verification

After deployment:

1. **Backend Health Check**:
   ```
   curl https://cb-data-factory-backend.onrender.com/
   ```
   Should return: `{"status":"healthy",...}`

2. **Frontend Check**:
   ```
   curl https://cb-data-factory-frontend.onrender.com/
   ```
   Should return the HTML page

## Troubleshooting

If builds still fail:

1. **Check Logs**: Click "View Logs" in Render dashboard
2. **Common Issues**:
   - Missing `GROQ_API_KEY`: Add it in Environment Variables
   - Wrong paths: Ensure Root Directory is set correctly
   - Memory limits: Free tier has 512MB RAM limit

## Files Summary

### Backend (`backend/`)
- ✅ `Dockerfile` - Clean, production-ready
- ✅ `.dockerignore` - Excludes venv, cache, etc.
- ✅ `requirements.txt` - Pinned stable versions
- ✅ `src/config.py` - No build-time validation

### Frontend (`frontend_new/`)
- ✅ `Dockerfile` - Multi-stage build with standalone output
- ✅ `.dockerignore` - Excludes node_modules
- ✅ `next.config.ts` - Standalone output enabled
- ✅ `package.json` - All dependencies locked

### Root
- ✅ `render.yaml` - Correct paths (relative to repo root)
