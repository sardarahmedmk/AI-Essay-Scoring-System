Write-Host "========================================" -ForegroundColor Green
Write-Host "   🚀 ESSAY SCORING SERVER (OPTIMIZED)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting optimized server with caching..." -ForegroundColor Yellow
Write-Host "Server will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features:" -ForegroundColor White
Write-Host "✅ 10-80x faster scoring" -ForegroundColor Green
Write-Host "✅ 5-minute result caching" -ForegroundColor Green
Write-Host "✅ Enhanced error handling" -ForegroundColor Green
Write-Host "✅ Colorful UI with animations" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Set-Location "d:\Downloads\Automatic-Essay-Scoring-master"

try {
    & "D:\Downloads\Automatic-Essay-Scoring-master\.venv\Scripts\python.exe" site_optimized.py
} catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host "Trying fallback simple server..." -ForegroundColor Yellow
    & "D:\Downloads\Automatic-Essay-Scoring-master\.venv\Scripts\python.exe" simple_server.py
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "Server stopped." -ForegroundColor Red
Read-Host "Press Enter to close"
