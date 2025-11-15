# Mount NAS manually for direct access
param(
    [string]$NASPath = "\\BernHQ\Big Pool\Shared Folders\Meshroom",
    [string]$LocalMount = "C:\meshroom-nas",
    [string]$Username = "bernardo"
)

Write-Host "Mounting NAS for Meshroom access..." -ForegroundColor Green

# Create local mount point
if (-not (Test-Path $LocalMount)) {
    New-Item -ItemType Directory -Path $LocalMount -Force
    Write-Host "Created mount point: $LocalMount" -ForegroundColor Green
}

# Prompt for password
$password = Read-Host "Enter password for $Username" -AsSecureString
$credential = New-Object System.Management.Automation.PSCredential($Username, $password)

try {
    # Map network drive
    New-PSDrive -Name "MeshroomNAS" -PSProvider FileSystem -Root $NASPath -Credential $credential -Persist
    
    # Create symbolic link for easy access
    if (-not (Test-Path "$LocalMount\data")) {
        New-Item -ItemType SymbolicLink -Path "$LocalMount\data" -Target $NASPath -Force
    }
    
    Write-Host "NAS mounted successfully!" -ForegroundColor Green
    Write-Host "Access via: $LocalMount\data" -ForegroundColor Cyan
    Write-Host "Direct path: $NASPath" -ForegroundColor Cyan
    
    # Create subdirectories if they don't exist
    $subdirs = @("input", "output", "temp", "logs")
    foreach ($subdir in $subdirs) {
        $nasSubdir = Join-Path $NASPath $subdir
        if (-not (Test-Path $nasSubdir)) {
            New-Item -ItemType Directory -Path $nasSubdir -Force
            Write-Host "Created: $subdir" -ForegroundColor Yellow
        }
    }
    
} catch {
    Write-Host "Failed to mount NAS: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "   - NAS is accessible from this PC" -ForegroundColor White
    Write-Host "   - Username/password are correct" -ForegroundColor White
    Write-Host "   - SMB sharing is enabled on NAS" -ForegroundColor White
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Copy photos to: $NASPath\input" -ForegroundColor White
Write-Host "   2. Both PCs will access the same data" -ForegroundColor White
Write-Host "   3. Results will be saved to: $NASPath\output" -ForegroundColor White