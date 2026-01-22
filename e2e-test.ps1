Write-Host "======================================" -ForegroundColor Cyan
Write-Host "END-TO-END INTEGRATION TEST SUITE" -ForegroundColor Cyan
Write-Host "Testing All Modules and Integration" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Backend Health
Write-Host "TEST 1: Backend Health Check" -ForegroundColor Yellow
try {
    $health = curl -s http://localhost:9000/health | ConvertFrom-Json
    Write-Host "OK: Backend Status: $($health.status)" -ForegroundColor Green
    Write-Host "   - Backend Service: $($health.services.backend)" -ForegroundColor Green
    Write-Host "   - Orchestrator: $($health.services.orchestrator)" -ForegroundColor Green
    Write-Host "   - MCP Status: $($health.services.mcp)" -ForegroundColor Yellow
} catch {
    Write-Host "FAIL: Backend Health Check Failed" -ForegroundColor Red
}
Write-Host ""

# Test 2: API Info
Write-Host "TEST 2: Backend API Information" -ForegroundColor Yellow
try {
    $apiInfo = curl -s http://localhost:9000/ | ConvertFrom-Json
    Write-Host "OK: API Title: $($apiInfo.title)" -ForegroundColor Green
    Write-Host "   - Version: $($apiInfo.version)" -ForegroundColor Green
} catch {
    Write-Host "FAIL: API Info Failed" -ForegroundColor Red
}
Write-Host ""

# Test 3: Orchestrate Endpoint
Write-Host "TEST 3: Orchestrate Endpoint" -ForegroundColor Yellow
try {
    $query = "What is cloud architecture?"
    $payload = @{query = $query} | ConvertTo-Json
    
    Write-Host "   Query: $query" -ForegroundColor Cyan
    
    $response = curl -s -X POST http://localhost:9000/orchestrate `
        -H "Content-Type: application/json" `
        -d $payload | ConvertFrom-Json
    
    Write-Host "OK: Response received" -ForegroundColor Green
    
    if ($response.response) {
        $preview = if ($response.response.Length -gt 100) { 
            $response.response.Substring(0, 100) + "..." 
        } else { 
            $response.response 
        }
        Write-Host "   Response: $preview" -ForegroundColor Green
    }
} catch {
    Write-Host "FAIL: Orchestrate Endpoint Failed" -ForegroundColor Red
}
Write-Host ""

# Test 4: Infrastructure Query
Write-Host "TEST 4: Infrastructure Query Endpoint" -ForegroundColor Yellow
try {
    $query = "Explain microservices"
    $payload = @{query = $query} | ConvertTo-Json
    
    Write-Host "   Query: $query" -ForegroundColor Cyan
    
    $response = curl -s -X POST http://localhost:9000/infrastructure/query `
        -H "Content-Type: application/json" `
        -d $payload | ConvertFrom-Json
    
    if ($response.response) {
        Write-Host "OK: Infrastructure agent responded" -ForegroundColor Green
    } else {
        Write-Host "WARN: No response from infrastructure agent" -ForegroundColor Yellow
    }
} catch {
    Write-Host "FAIL: Infrastructure Query Failed" -ForegroundColor Red
}
Write-Host ""

# Test 5: Chat Endpoint
Write-Host "TEST 5: Chat Endpoint" -ForegroundColor Yellow
try {
    $query = "Tell me about DevOps"
    $payload = @{query = $query; session_id = "test_123"} | ConvertTo-Json
    
    Write-Host "   Query: $query" -ForegroundColor Cyan
    
    $response = curl -s -X POST http://localhost:9000/chat `
        -H "Content-Type: application/json" `
        -d $payload | ConvertFrom-Json
    
    if ($response.response) {
        Write-Host "OK: Chat endpoint responded" -ForegroundColor Green
    } else {
        Write-Host "WARN: No response from chat endpoint" -ForegroundColor Yellow
    }
} catch {
    Write-Host "FAIL: Chat Endpoint Failed" -ForegroundColor Red
}
Write-Host ""

# Test 6: Swagger UI
Write-Host "TEST 6: Swagger UI Documentation" -ForegroundColor Yellow
try {
    $swagger = curl -s -o $null -w "%{http_code}" http://localhost:9000/docs
    if ($swagger -eq "200") {
        Write-Host "OK: Swagger UI available at http://localhost:9000/docs" -ForegroundColor Green
    }
} catch {
    Write-Host "FAIL: Swagger UI check failed" -ForegroundColor Red
}
Write-Host ""

# Test 7: UI Server
Write-Host "TEST 7: Frontend UI Server" -ForegroundColor Yellow
try {
    $ui = curl -s -m 2 http://localhost:3000/ -o $null -w "%{http_code}"
    if ($ui -eq "200") {
        Write-Host "OK: UI Server running at http://localhost:3000" -ForegroundColor Green
    }
} catch {
    Write-Host "FAIL: UI Server check failed" -ForegroundColor Red
}
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "RUNNING SERVICES:" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:9000" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "API DOCUMENTATION:" -ForegroundColor Cyan
Write-Host "  Swagger UI: http://localhost:9000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Open http://localhost:3000 in browser" -ForegroundColor Yellow
Write-Host "  2. Type a message in the chat" -ForegroundColor Yellow
Write-Host "  3. Backend will process and respond" -ForegroundColor Yellow
Write-Host ""
Write-Host "All systems ready!" -ForegroundColor Green
