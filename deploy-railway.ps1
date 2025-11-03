# Quick Deployment Script for Railway
# Run this after installing Railway CLI: npm i -g @railway/cli

Write-Host "🚀 Deploying Task Reminder Agent to Railway..." -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Railway CLI not found!" -ForegroundColor Red
    Write-Host "Install it with: npm i -g @railway/cli" -ForegroundColor Yellow
    exit 1
}

# Login to Railway
Write-Host "📝 Logging into Railway..." -ForegroundColor Green
railway login

# Initialize project
Write-Host "🔧 Initializing Railway project..." -ForegroundColor Green
railway init

# Deploy
Write-Host "🚀 Deploying to Railway..." -ForegroundColor Green
railway up

# Get status
Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Getting deployment status..." -ForegroundColor Cyan
railway status

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Copy your Railway URL from above"
Write-Host "2. Edit telex-workflow.json and replace YOUR_DEPLOYED_URL"
Write-Host "3. Set TELEX_WEBHOOK_URL: railway variables set TELEX_WEBHOOK_URL=<your-telex-webhook>"
Write-Host "4. Upload telex-workflow.json to Telex"
Write-Host "5. Test your agent!"
Write-Host ""
Write-Host "📚 See TELEX_INTEGRATION.md for detailed instructions"
