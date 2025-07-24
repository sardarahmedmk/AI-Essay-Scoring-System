# 🚀 GitHub Upload Preparation Script
# Author: Sardar Ahmed
# Description: Prepares Essay Scoring System for GitHub upload

Write-Host "🚀 Preparing Essay Scoring System for GitHub Upload..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Get current directory
$currentDir = Get-Location
Write-Host "📁 Current directory: $currentDir" -ForegroundColor Yellow

# List all files to be uploaded
Write-Host "`n📋 Files ready for GitHub upload:" -ForegroundColor Green
Get-ChildItem -Path . -File | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  ✅ $($_.Name) ($size KB)" -ForegroundColor White
}

Write-Host "`n📂 Directories:" -ForegroundColor Green
Get-ChildItem -Path . -Directory | ForEach-Object {
    Write-Host "  📁 $($_.Name)/" -ForegroundColor White
    Get-ChildItem -Path $_.FullName -File | ForEach-Object {
        $size = [math]::Round($_.Length / 1KB, 2)
        Write-Host "    ✅ $($_.Name) ($size KB)" -ForegroundColor Gray
    }
}

# Check for important files
Write-Host "`n🔍 Checking required files..." -ForegroundColor Green
$requiredFiles = @("README.md", "LICENSE", ".gitignore", "requirements.txt", "site_optimized.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (Missing)" -ForegroundColor Red
    }
}

# Calculate total size
$totalSize = (Get-ChildItem -Path . -Recurse -File | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)
Write-Host "`n📊 Total project size: $totalSizeMB MB" -ForegroundColor Cyan

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create 'Essay-Scoring-System' folder in your Machine-Learning repo" -ForegroundColor White
Write-Host "2. Copy all these files to that folder" -ForegroundColor White
Write-Host "3. Commit and push to GitHub" -ForegroundColor White
Write-Host "4. Update your main README.md with project link" -ForegroundColor White

Write-Host "`n🔗 Your GitHub repository:" -ForegroundColor Cyan
Write-Host "   https://github.com/sardarahmedmk/Machine-Learning" -ForegroundColor Blue

Write-Host "`n✨ Ready for upload! Your professional Essay Scoring System is prepared." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Optional: Open GitHub in browser
$openGitHub = Read-Host "`nOpen GitHub repository in browser? (y/n)"
if ($openGitHub -eq 'y' -or $openGitHub -eq 'Y') {
    Start-Process "https://github.com/sardarahmedmk/Machine-Learning"
}
