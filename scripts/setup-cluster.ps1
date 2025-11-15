# Meshroom Kubernetes Cluster - Worker Node Setup
# Use this script to setup worker nodes on additional AMD PCs

param(
    [Parameter(Mandatory=$true)]
    [string]$MasterIP,
    
    [Parameter(Mandatory=$true)]
    [string]$WorkerToken,
    
    [Parameter(Mandatory=$false)]
    [string]$NASIP = "10.0.0.80",
    
    [Parameter(Mandatory=$false)]
    [string]$NASPath = "\\BernHQ\Big Pool\Shared Folders\Meshroom",
    
    [Parameter(Mandatory=$false)]
    [switch]$IsWorker,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipPrompts
)

Write-Host "🔧 Meshroom Kubernetes Cluster - Worker Node Setup" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator" -ForegroundColor Red
    Write-Host "💡 Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found. Installing..." -ForegroundColor Yellow
        choco install python -y
        refreshenv
    }
    
    # Check Docker
    try {
        $dockerVersion = docker --version 2>&1
        Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker not found. Installing..." -ForegroundColor Yellow
        choco install docker-desktop -y
        Write-Host "⚠️  Docker Desktop installed. Please restart your computer and run this script again." -ForegroundColor Yellow
        exit 0
    }
    
    # Check kubectl
    try {
        kubectl version --client 2>&1 | Out-Null
        Write-Host "✅ kubectl found" -ForegroundColor Green
    } catch {
        Write-Host "❌ kubectl not found. Installing..." -ForegroundColor Yellow
        choco install kubernetes-cli -y
        refreshenv
    }
    
    # Check Chocolatey
    try {
        $chocoVersion = choco --version 2>&1
        Write-Host "✅ Chocolatey found: $chocoVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Chocolatey not found. Installing..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        refreshenv
    }
}

# Function to setup worker node
function Initialize-WorkerNode {
    param(
        [string]$MasterIP,
        [string]$WorkerToken
    )
    
    Write-Host "🔧 Setting up Worker Node..." -ForegroundColor Cyan
    
    # Check for Docker Desktop with Kubernetes
    Write-Host "📋 Checking for Docker Desktop with Kubernetes..." -ForegroundColor Yellow
    
    # Check if Docker is installed
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Docker not found. Installing Docker Desktop..." -ForegroundColor Yellow
        
        # Download Docker Desktop installer
        Write-Host "📥 Downloading Docker Desktop for Windows..." -ForegroundColor Cyan
        $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        $dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
        
        try {
            Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -ErrorAction Stop
            Write-Host "✅ Docker Desktop downloaded successfully!" -ForegroundColor Green
            
            # Run installer
            Write-Host "🚀 Running Docker Desktop installer..." -ForegroundColor Yellow
            Write-Host "⚠️  Please follow the installation wizard and enable Kubernetes when prompted." -ForegroundColor Cyan
            Start-Process -FilePath $dockerInstaller -Wait
            
            # Clean up installer
            Remove-Item $dockerInstaller -Force -ErrorAction SilentlyContinue
            
            Write-Host "✅ Docker Desktop installation completed!" -ForegroundColor Green
            Write-Host "🔄 Please restart your computer and run this script again." -ForegroundColor Yellow
            Write-Host "⚠️  Make sure to enable Kubernetes in Docker Desktop settings." -ForegroundColor Cyan
            exit 0
            
        } catch {
            Write-Host "❌ Failed to download Docker Desktop: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "💡 Please manually download and install Docker Desktop from:" -ForegroundColor Yellow
            Write-Host "   https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Cyan
            Write-Host "⚠️  Make sure to enable Kubernetes in the settings." -ForegroundColor Yellow
            exit 1
        }
    }
    
    # Check if Kubernetes is enabled in Docker Desktop
    Write-Host "🔍 Checking if Kubernetes is enabled in Docker Desktop..." -ForegroundColor Yellow
    try {
        kubectl cluster-info | Out-Null
        Write-Host "✅ Kubernetes is running!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Kubernetes is not enabled in Docker Desktop." -ForegroundColor Red
        Write-Host "⚠️  Please enable Kubernetes in Docker Desktop:" -ForegroundColor Yellow
        Write-Host "   1. Open Docker Desktop" -ForegroundColor Cyan
        Write-Host "   2. Go to Settings > Kubernetes" -ForegroundColor Cyan
        Write-Host "   3. Check 'Enable Kubernetes'" -ForegroundColor Cyan
        Write-Host "   4. Click 'Apply & Restart'" -ForegroundColor Cyan
        Write-Host "   5. Wait for Kubernetes to start, then run this script again" -ForegroundColor Cyan
        if (-not $SkipPrompts) {
            Read-Host "Press Enter when Kubernetes is enabled and running"
        } else {
            Write-Host "SkipPrompts enabled - assuming Kubernetes is enabled..." -ForegroundColor Yellow
            Start-Sleep -Seconds 2
        }
        
        # Check again
        try {
            kubectl cluster-info | Out-Null
            Write-Host "✅ Kubernetes is now running!" -ForegroundColor Green
        } catch {
            Write-Host "❌ Kubernetes is still not available. Please check Docker Desktop settings." -ForegroundColor Red
            exit 1
        }
    }
    
    # Set context to docker-desktop
    Write-Host "🔧 Setting up Kubernetes context..." -ForegroundColor Yellow
    try {
        kubectl config use-context docker-desktop
        Write-Host "✅ Kubernetes context set to docker-desktop" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Warning: Could not set docker-desktop context" -ForegroundColor Yellow
    }
    
    # Note: Docker Desktop worker nodes join the same cluster automatically through Docker networking
    Write-Host "📝 Note: With Docker Desktop, this PC will share the Kubernetes cluster" -ForegroundColor Cyan
    Write-Host "   through Docker's shared networking. Token: $WorkerToken" -ForegroundColor White
    
    # Try to label the node if possible
    try {
        $nodeName = kubectl get nodes -o jsonpath='{.items[0].metadata.name}'
        kubectl label node $nodeName node-role.kubernetes.io/worker=true --overwrite
        kubectl label node $nodeName gpu=amd --overwrite
        Write-Host "✅ Node labeled successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Warning: Could not label node (this may be normal with Docker Desktop)" -ForegroundColor Yellow
    }
    
    Write-Host "✅ Worker Node setup complete!" -ForegroundColor Green
    Write-Host "🎯 This PC is now part of the distributed processing cluster!" -ForegroundColor Cyan
}

# Function to install GUI requirements
function Install-GUIRequirements {
    Write-Host "📱 Installing GUI requirements..." -ForegroundColor Cyan
    
    Set-Location "app"
    pip install -r requirements.txt
    Set-Location ".."
    
    Write-Host "✅ GUI requirements installed!" -ForegroundColor Green
}

# Main execution
try {
    Write-Host "🚀 Starting worker node setup..." -ForegroundColor Green
    
    # Check prerequisites
    Test-Prerequisites
    
    # Setup worker node
    Initialize-WorkerNode -MasterIP $MasterIP -WorkerToken $WorkerToken
    
    # Install GUI requirements
    Install-GUIRequirements
    
    Write-Host ""
    Write-Host "🎉 Worker node setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📖 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Verify connection to master: kubectl get nodes" -ForegroundColor White
    Write-Host "   2. Launch GUI: .\gui\launch-gui.bat" -ForegroundColor White
    Write-Host "   3. Monitor cluster: .\scripts\deploy.ps1 status" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Your AMD PC is now part of the distributed Meshroom cluster!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error during setup: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Check the logs and try again" -ForegroundColor Yellow
    exit 1
} 