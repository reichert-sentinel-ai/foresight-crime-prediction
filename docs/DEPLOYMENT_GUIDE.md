# Live Demo Deployment Guide

**Repository**: Foresight Crime Prediction  
**Date**: December 2024  
**Status**: Complete

---

## Quick Deploy to Streamlit Cloud

### Step 1: Prepare Repository

```bash
cd project/repo-foresight

# Ensure requirements.txt includes:
# streamlit>=1.28.0
# fastapi>=0.104.0
# prophet>=1.1.0
# etc.

# Ensure streamlit_app.py exists in root
```

### Step 2: Deploy

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `reichert-sentinel-ai/foresight-crime-prediction`
5. Main file: `streamlit_app.py`
6. Branch: `main`
7. Click "Deploy"

### Step 3: Configure Environment

Add environment variables in Streamlit Cloud:
- `MAPBOX_ACCESS_TOKEN`: Your Mapbox access token
- `FORESIGHT_DB_URL`: PostgreSQL connection string
- `FORESIGHT_REDIS_URL`: Redis connection string (optional)

### Step 4: Access Demo

URL: `https://foresight-crime-prediction.streamlit.app`

---

## Docker Deployment

```bash
# Build
docker build -t foresight:latest .

# Run
docker run -p 8501:8501 \
  -e MAPBOX_ACCESS_TOKEN=your_token \
  -e FORESIGHT_DB_URL=postgresql://... \
  foresight:latest
```

---

## Environment Variables

```bash
MAPBOX_ACCESS_TOKEN=your_mapbox_token
FORESIGHT_DB_URL=postgresql://user:pass@host:5432/foresight
FORESIGHT_REDIS_URL=redis://localhost:6379
CHICAGO_DATA_URL=https://data.cityofchicago.org/...
```

---

*See [Guardian Deployment Guide](../repo-guardian/docs/DEPLOYMENT_GUIDE.md) for detailed deployment options.*

