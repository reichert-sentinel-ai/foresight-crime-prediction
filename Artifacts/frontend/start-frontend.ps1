# Frontend Setup and Start Script
# Run this script to install dependencies and start the frontend server

Write-Host "=== Foresight Frontend Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Node.js is not installed!" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
Write-Host ""

# Check if npm is installed
Write-Host "Checking npm installation..." -ForegroundColor Yellow
$npmVersion = npm --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: npm is not installed!" -ForegroundColor Red
    exit 1
}
Write-Host "npm version: $npmVersion" -ForegroundColor Green
Write-Host ""

# Check if node_modules exists
if (Test-Path "node_modules") {
    Write-Host "Dependencies already installed. Skipping npm install." -ForegroundColor Green
} else {
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm install failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
}
Write-Host ""

# Check if backend is running
Write-Host "Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Backend server is running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Backend server may not be running on port 8000" -ForegroundColor Yellow
    Write-Host "Make sure to start the backend with: python -m uvicorn src.api.main:app --port 8000" -ForegroundColor Yellow
}
Write-Host ""

# Start the frontend server
Write-Host "Starting frontend development server..." -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:5173/crime-map" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

npm run dev

