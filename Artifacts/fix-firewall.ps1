# PowerShell script to allow Vite dev server through Windows Firewall
# Run this script as Administrator

Write-Host "Adding Windows Firewall rule for Vite Dev Server (port 5173)..." -ForegroundColor Yellow

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Remove existing rule if it exists
try {
    Remove-NetFirewallRule -DisplayName "Vite Dev Server" -ErrorAction SilentlyContinue
    Write-Host "Removed existing rule (if any)" -ForegroundColor Gray
} catch {
    # Ignore if rule doesn't exist
}

# Add new firewall rule
try {
    New-NetFirewallRule -DisplayName "Vite Dev Server" `
        -Direction Inbound `
        -LocalPort 5173 `
        -Protocol TCP `
        -Action Allow `
        -Description "Allow Vite development server on port 5173" | Out-Null
    
    Write-Host "SUCCESS: Firewall rule added for port 5173!" -ForegroundColor Green
    Write-Host "You can now access the dev server from your phone." -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to add firewall rule" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Your server should be accessible at:" -ForegroundColor Cyan
Write-Host "  http://192.168.1.161:5173/crime-map" -ForegroundColor White

