# Test A2A Endpoint
# This script tests your Task Reminder Agent's A2A protocol endpoint

param(
    [Parameter(Mandatory=$false)]
    [string]$Url = "http://localhost:9000"
)

Write-Host "🧪 Testing Task Reminder Agent A2A Endpoint" -ForegroundColor Cyan
Write-Host "URL: $Url/a2a/agent/taskAgent" -ForegroundColor Gray
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "$Url/" -Method GET | ConvertFrom-Json
    Write-Host "✅ Server is online: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Server is not responding!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: Create Task with A2A Protocol
Write-Host "Test 2: Create Task via A2A" -ForegroundColor Yellow
$body = @{
    message = "remind me at 5pm to study"
    user = "test-user"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$Url/a2a/agent/taskAgent" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body | ConvertFrom-Json
    
    if ($response.success) {
        Write-Host "✅ Task created successfully!" -ForegroundColor Green
        Write-Host "   Response: $($response.response)" -ForegroundColor Gray
        Write-Host "   Agent: $($response.agent)" -ForegroundColor Gray
        Write-Host "   Timestamp: $($response.timestamp)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Failed to create task" -ForegroundColor Red
        Write-Host "   Error: $($response.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Request failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
Write-Host ""

# Test 3: Create Task with Natural Time
Write-Host "Test 3: Natural Language Time" -ForegroundColor Yellow
$body2 = @{
    message = "remind me tomorrow at 3pm to call mom"
    user = "test-user"
} | ConvertTo-Json

try {
    $response2 = Invoke-WebRequest -Uri "$Url/a2a/agent/taskAgent" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body2 | ConvertFrom-Json
    
    if ($response2.success) {
        Write-Host "✅ Task created successfully!" -ForegroundColor Green
        Write-Host "   Response: $($response2.response)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Request failed!" -ForegroundColor Red
}
Write-Host ""

# Test 4: List Tasks
Write-Host "Test 4: List All Tasks" -ForegroundColor Yellow
try {
    $tasks = Invoke-WebRequest -Uri "$Url/tasks?user=test-user" -Method GET | ConvertFrom-Json
    Write-Host "✅ Retrieved $($tasks.count) tasks" -ForegroundColor Green
    
    if ($tasks.tasks.Count -gt 0) {
        Write-Host ""
        Write-Host "   Tasks:" -ForegroundColor Gray
        foreach ($task in $tasks.tasks) {
            Write-Host "   - Task #$($task.id): $($task.task) at $($task.time)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "❌ Failed to retrieve tasks" -ForegroundColor Red
}
Write-Host ""

# Test 5: Invalid Message
Write-Host "Test 5: Error Handling (Empty Message)" -ForegroundColor Yellow
$body3 = @{
    message = ""
    user = "test-user"
} | ConvertTo-Json

try {
    $response3 = Invoke-WebRequest -Uri "$Url/a2a/agent/taskAgent" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body3 | ConvertFrom-Json
    
    if (-not $response3.success) {
        Write-Host "✅ Error handling works correctly" -ForegroundColor Green
        Write-Host "   Error: $($response3.error)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Request failed unexpectedly" -ForegroundColor Red
}
Write-Host ""

Write-Host "🎉 Testing Complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Deploy to Railway/Render/Fly.io"
Write-Host "2. Update telex-workflow.json with your deployed URL"
Write-Host "3. Register agent in Telex"
Write-Host "4. Test via Telex chat interface"
Write-Host ""
Write-Host "📚 See TELEX_INTEGRATION.md for deployment instructions"
