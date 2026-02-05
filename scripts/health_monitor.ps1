# CheckBhai Health Monitor
# Monitors backend health and sends alerts on failure

$baseUrl = "https://checkbhai.onrender.com"
$logFile = "health_monitor.log"
$checkInterval = 300  # 5 minutes

function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry -ForegroundColor $(if ($Level -eq "ERROR") { "Red" } elseif ($Level -eq "WARN") { "Yellow" } else { "White" })
    Add-Content -Path $logFile -Value $logEntry
}

function Test-Backend {
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing -TimeoutSec 90
        $stopwatch.Stop()
        
        $data = $response.Content | ConvertFrom-Json
        
        if ($data.status -eq "ok") {
            Write-Log "Health check PASSED in $($stopwatch.ElapsedMilliseconds)ms"
            return @{ success = $true; latency = $stopwatch.ElapsedMilliseconds }
        } else {
            Write-Log "Health check returned unexpected status: $($data.status)" "WARN"
            return @{ success = $false; latency = $stopwatch.ElapsedMilliseconds }
        }
    } catch {
        Write-Log "Health check FAILED: $_" "ERROR"
        return @{ success = $false; error = $_.Exception.Message }
    }
}

function Test-ScamDetection {
    try {
        $testMessage = '{"message": "URGENT: Send money to claim prize!"}'
        $response = Invoke-WebRequest -Uri "$baseUrl/check/message" -Method POST -Body $testMessage -ContentType "application/json" -UseBasicParsing -TimeoutSec 30
        $data = $response.Content | ConvertFrom-Json
        
        if ($data.risk_level) {
            Write-Log "Scam detection working: risk_level=$($data.risk_level)"
            return $true
        } else {
            Write-Log "Scam detection returned no risk_level" "WARN"
            return $false
        }
    } catch {
        Write-Log "Scam detection test FAILED: $_" "ERROR"
        return $false
    }
}

# Main monitoring loop
Write-Log "========================================" 
Write-Log "CheckBhai Health Monitor Started"
Write-Log "Backend: $baseUrl"
Write-Log "Interval: ${checkInterval}s"
Write-Log "========================================"

$consecutiveFailures = 0
$maxFailures = 3

while ($true) {
    $healthResult = Test-Backend
    
    if ($healthResult.success) {
        $consecutiveFailures = 0
        
        # Also test scam detection periodically
        if ((Get-Random -Maximum 4) -eq 0) {
            Test-ScamDetection
        }
    } else {
        $consecutiveFailures++
        
        if ($consecutiveFailures -ge $maxFailures) {
            Write-Log "ALERT: Backend has failed $consecutiveFailures consecutive health checks!" "ERROR"
            # Here you could add: Send email, Slack notification, etc.
        }
    }
    
    Start-Sleep -Seconds $checkInterval
}
