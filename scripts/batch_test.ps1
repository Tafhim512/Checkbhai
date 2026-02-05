# CheckBhai Batch Test Script
# Run comprehensive tests on the scam detection API

$baseUrl = "https://checkbhai.onrender.com"

# Test messages array
$testMessages = @(
    # SCAM MESSAGES
    @{
        category = "SCAM - Phishing"
        message = "URGENT! Your bKash account will be suspended. Call 01700000000 and give your PIN to verify."
        expected = "High"
    },
    @{
        category = "SCAM - Lottery"
        message = "Congratulations! You won 500000 Taka lottery. Send 5000 Taka processing fee to claim prize immediately."
        expected = "High"
    },
    @{
        category = "SCAM - Job Fraud (Bangla)"
        message = "আপনি ঘরে বসে মাসে ৫০০০০ টাকা আয় করতে পারবেন। এখনই ২০০০ টাকা পাঠান এবং শুরু করুন।"
        expected = "High"
    },
    @{
        category = "SCAM - Romance/Advance Fee"
        message = "I am stuck at airport customs. Please send 10000 taka to this bKash number urgently, I will pay back double tomorrow."
        expected = "High"
    },
    
    # NORMAL MESSAGES
    @{
        category = "NORMAL - Business"
        message = "Hi, I am interested in buying your product. Can you share more details about pricing and delivery?"
        expected = "Low"
    },
    @{
        category = "NORMAL - Casual"
        message = "Bhai, ki obostha? Ajke Football match dekhbi? Amar bari chole ay."
        expected = "Low"
    },
    @{
        category = "NORMAL - Legitimate payment"
        message = "Please send 500 taka for the groceries we bought yesterday. My bKash is 01712345678."
        expected = "Low"
    },
    
    # EDGE CASES
    @{
        category = "EDGE - Special characters"
        message = "Test with special chars: @#$%^&*()_+{}|:<>? emoji: 🎉💰🚨"
        expected = "Low"
    },
    @{
        category = "EDGE - Numbers only"
        message = "01711111111 01822222222 50000 100000 999999"
        expected = "Low"
    },
    @{
        category = "EDGE - Long message"
        message = "This is a very long message to test the system. " * 20
        expected = "Low"
    }
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CHECKBHAI BATCH TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# First, wake up the backend
Write-Host "Waking up backend (may take 30-60 seconds on cold start)..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing -TimeoutSec 90
    Write-Host "Backend is AWAKE: $($health.Content)`n" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Backend not responding: $_`n" -ForegroundColor Red
    exit 1
}

$results = @()
$passed = 0
$failed = 0

foreach ($test in $testMessages) {
    Write-Host "Testing: $($test.category)" -ForegroundColor White
    
    try {
        $body = @{ message = $test.message } | ConvertTo-Json
        $response = Invoke-WebRequest -Uri "$baseUrl/check/message" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 30
        $data = $response.Content | ConvertFrom-Json
        
        $status = if ($data.risk_level -eq $test.expected) { "PASS" } else { "CHECK" }
        $color = if ($status -eq "PASS") { "Green" } else { "Yellow" }
        
        Write-Host "  Result: $($data.risk_level) (expected: $($test.expected)) - $status" -ForegroundColor $color
        Write-Host "  Red Flags: $($data.red_flags -join ', ')" -ForegroundColor Gray
        
        if ($status -eq "PASS") { $passed++ } else { $failed++ }
        
        $results += @{
            Category = $test.category
            Expected = $test.expected
            Actual = $data.risk_level
            Status = $status
            RedFlags = $data.red_flags -join ", "
        }
    } catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
        $failed++
        $results += @{
            Category = $test.category
            Expected = $test.expected
            Actual = "ERROR"
            Status = "FAIL"
            RedFlags = $_.Exception.Message
        }
    }
    
    Write-Host ""
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "To Check: $failed" -ForegroundColor Yellow
Write-Host "Total: $($testMessages.Count)" -ForegroundColor White

# Export results
$results | Export-Csv -Path "batch_test_results.csv" -NoTypeInformation
Write-Host "`nResults saved to: batch_test_results.csv" -ForegroundColor Gray
