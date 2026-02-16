# Quick Fix: Deploy Without Blueprint

## The Issue
Render Blueprint is having trouble with the monorepo structure. The solution is to deploy each service individually.

## Step-by-Step Fix

### 1. Delete Current Blueprint Services
1. Go to Render Dashboard
2. Delete both `cb-data-factory-backend` and `cb-data-factory-frontend` services
3. This clears all cached configurations

### 2. Deploy Backend (Do This First)

1. Click **New +** → **Web Service**
2. **Connect Repository**: Select `Vishal14367/CB-Data-Factory`
3. **Configure Service**:
   ```
   Name: cb-data-factory-backend
   Region: Singapore
   Branch: main
   Root Directory: backend
   Runtime: Docker
   Dockerfile Path: Dockerfile
   Docker Build Context Directory: .
   ```

4. **Environment Variables** (click "Add Environment Variable"):
   ```
   GROQ_API_KEY = <paste-your-key-here>
   HOST = 0.0.0.0  
   PORT = 10000
   ```

5. **Instance Type**: Free
6. Click **Create Web Service**
7. **Wait for deployment** (5-10 minutes)
8. **Copy the URL** (e.g., `https://cb-data-factory-backend.onrender.com`)

### 3. Deploy Frontend (After Backend is Live)

1. Click **New +** → **Web Service**  
2. **Connect Repository**: Same repo `Vishal14367/CB-Data-Factory`
3. **Configure Service**:
   ```
   Name: cb-data-factory-frontend
   Region: Singapore
   Branch: main
   Root Directory: frontend_new
   Runtime: Docker
   Dockerfile Path: Dockerfile
   Docker Build Context Directory: .
   ```

4. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL = https://cb-data-factory-backend.onrender.com
   ```
   *(Use the URL you copied from Step 2)*

5. **Instance Type**: Free
6. Click **Create Web Service**
7. **Wait for deployment** (5-10 minutes)

### 4. Test Your Application

1. Open the frontend URL: `https://cb-data-factory-frontend.onrender.com`
2. You should see your application!

## Why This Works

- **No Blueprint complexity**: Render handles each service independently
- **Correct paths**: Root Directory + Dockerfile Path work together
- **No caching issues**: Fresh deployment from scratch
- **Proper env vars**: Backend URL is hardcoded in frontend build

## If It Still Fails

Check the build logs:
1. Click on the failing service
2. Click **Logs** tab
3. Look for the actual error message
4. Common issues:
   - **Out of memory**: Free tier has 512MB limit
   - **Missing dependencies**: Check if all packages install
   - **Build timeout**: Free tier has 15-minute build limit

## Alternative: Use Render's Native Runtime

If Docker builds keep failing due to memory limits, you can try:

### Backend (Native Python):
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Native Node):
```
Runtime: Node
Build Command: npm install && npm run build
Start Command: npm start
```

This uses less memory than Docker builds.
