# Coolify Deployment Guide

## What this app needs
- **Backend** (Python/FastAPI) — runs the AI data generation engine
- **Frontend** (Next.js) — the web interface users see
- Both run together via Docker Compose

---

## Step 1 — Push your code to GitHub
Make sure your latest code is pushed to GitHub.
(The `.env` file is excluded by git — that's correct. API keys go in Coolify, not GitHub.)

---

## Step 2 — Create a new project in Coolify

1. Log into your Coolify instance
2. Click **"New Project"** → give it a name (e.g. `CB Data Factory`)
3. Inside the project, click **"New Resource"**
4. Choose **"Docker Compose"**
5. Connect your GitHub account and select this repository

---

## Step 3 — Set Environment Variables

In Coolify, go to the **Environment Variables** section and add these:

### For the `backend` service:
| Variable | Value |
|---|---|
| `GROQ_API_KEY` | your actual Groq key (from console.groq.com) |
| `PORT` | `8000` |

> The other variables (DEFAULT_DIFFICULTY, etc.) have sensible defaults — you only need GROQ_API_KEY.

### For the `frontend` service:
| Variable | Value |
|---|---|
| `BACKEND_URL` | `http://backend:8000` |

> This is already set in docker-compose.yml — Coolify may pick it up automatically.

---

## Step 4 — Configure which port is public

In Coolify, set the **public port** to `3000` (the frontend).
The backend (port 8000) stays internal — users never access it directly.

---

## Step 5 — Deploy

Click **"Deploy"**. Coolify will:
1. Pull your code from GitHub
2. Build the Docker images (takes 3-5 minutes on first run)
3. Start both containers
4. Give you a public URL like `https://cb-data-factory.yourdomain.com`

---

## Step 6 — Share the link

That's it! Share the URL Coolify gives you with anyone on your team.

---

## Updating the app later

Whenever you push new code to GitHub:
- Go to Coolify → your project → click **"Redeploy"**
- Or enable **auto-deploy** in Coolify so it deploys automatically on every push

---

## Troubleshooting

**App shows error / blank page:**
- Check Coolify logs for the `backend` service — likely the `GROQ_API_KEY` is missing or wrong

**"502 Bad Gateway":**
- The backend is not running. Check backend logs in Coolify.

**Very slow first load:**
- Normal. The first dataset generation can take 60-90 seconds.
