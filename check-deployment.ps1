# Pre-Deployment Checklist Script
# Run this before deploying to ensure everything is ready

Write-Host "🚀 VIBEZ Pre-Deployment Checklist" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check 1: Git initialized
Write-Host "✓ Checking git repository..." -NoNewline
if (Test-Path ".git") {
    Write-Host " ✅ OK" -ForegroundColor Green
} else {
    Write-Host " ❌ FAIL - Run 'git init'" -ForegroundColor Red
    $allGood = $false
}

# Check 2: Files committed
Write-Host "✓ Checking git commits..." -NoNewline
$commitCount = git rev-list --count HEAD 2>$null
if ($commitCount -gt 0) {
    Write-Host " ✅ OK ($commitCount commits)" -ForegroundColor Green
} else {
    Write-Host " ❌ FAIL - No commits found" -ForegroundColor Red
    $allGood = $false
}

# Check 3: ML model exists
Write-Host "✓ Checking ML model..." -NoNewline
if (Test-Path "backend/models/vibe_classifier.pkl") {
    $modelSize = (Get-Item "backend/models/vibe_classifier.pkl").Length / 1MB
    Write-Host " ✅ OK ($([math]::Round($modelSize, 2)) MB)" -ForegroundColor Green
    if ($modelSize -gt 50) {
        Write-Host "  ⚠️  Warning: Model size > 50MB may fail on Vercel" -ForegroundColor Yellow
    }
} else {
    Write-Host " ❌ FAIL - Model not found. Run 'python backend/train_ml_model.py'" -ForegroundColor Red
    $allGood = $false
}

# Check 4: Backend dependencies
Write-Host "✓ Checking backend requirements.txt..." -NoNewline
if (Test-Path "backend/requirements.txt") {
    $reqCount = (Get-Content "backend/requirements.txt" | Measure-Object -Line).Lines
    Write-Host " ✅ OK ($reqCount packages)" -ForegroundColor Green
} else {
    Write-Host " ❌ FAIL - requirements.txt missing" -ForegroundColor Red
    $allGood = $false
}

# Check 5: Frontend dependencies
Write-Host "✓ Checking frontend package.json..." -NoNewline
if (Test-Path "frontend/package.json") {
    Write-Host " ✅ OK" -ForegroundColor Green
} else {
    Write-Host " ❌ FAIL - package.json missing" -ForegroundColor Red
    $allGood = $false
}

# Check 6: Frontend build works
Write-Host "✓ Checking frontend can build..." -NoNewline
Push-Location frontend
if (Test-Path "node_modules") {
    Write-Host " ✅ node_modules exists" -ForegroundColor Green
} else {
    Write-Host " ⚠️  node_modules not found - run 'npm install'" -ForegroundColor Yellow
}
Pop-Location

# Check 7: Vercel config
Write-Host "✓ Checking vercel.json..." -NoNewline
if (Test-Path "vercel.json") {
    Write-Host " ✅ OK" -ForegroundColor Green
} else {
    Write-Host " ❌ FAIL - vercel.json missing" -ForegroundColor Red
    $allGood = $false
}

# Check 8: .gitignore
Write-Host "✓ Checking .gitignore..." -NoNewline
if (Test-Path ".gitignore") {
    Write-Host " ✅ OK" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Warning - .gitignore missing" -ForegroundColor Yellow
}

# Check 9: Environment files
Write-Host "✓ Checking environment setup..." -NoNewline
if ((Test-Path ".env.example") -and (Test-Path "frontend/.env.production")) {
    Write-Host " ✅ OK" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Warning - env files missing" -ForegroundColor Yellow
}

# Check 10: Documentation
Write-Host "✓ Checking documentation..." -NoNewline
$docCount = 0
if (Test-Path "README.md") { $docCount++ }
if (Test-Path "DEPLOYMENT_GUIDE.md") { $docCount++ }
if (Test-Path "GITHUB_DEPLOY_GUIDE.md") { $docCount++ }
Write-Host " ✅ OK ($docCount files)" -ForegroundColor Green

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "🎉 All checks passed! Ready to deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Push to GitHub: See GITHUB_DEPLOY_GUIDE.md" -ForegroundColor White
    Write-Host "2. Deploy to Vercel: vercel --prod" -ForegroundColor White
    Write-Host "3. Test your live app!" -ForegroundColor White
} else {
    Write-Host "❌ Some checks failed. Please fix the issues above." -ForegroundColor Red
}

Write-Host ""
