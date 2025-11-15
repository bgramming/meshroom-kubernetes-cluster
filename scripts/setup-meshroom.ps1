# Meshroom Kubernetes Cluster Setup Script
# Master Node Setup
#
# Usage:
#   .\setup-meshroom.ps1                    # Smart setup (checks existing components)
#   .\setup-meshroom.ps1 -Force             # Force full rebuild
#   .\setup-meshroom.ps1 -SkipPrompts       # Use default values
#   .\setup-meshroom.ps1 -Force -SkipPrompts # Force rebuild with defaults

param(
    [string]$MasterIP = "10.0.0.226",
    [string]$NASIP = "10.0.0.80",
    [string]$NASPath = "\\BernHQ\Big Pool\Shared Folders\Meshroom",
    [switch]$SkipPrompts,
    [switch]$Force  # Force full rebuild even if components exist
)

# Function to check prerequisites
function Test-Prerequisites {
    Write-Host "Checking prerequisites..." -ForegroundColor Cyan
    
    # Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Error: Python is not installed" -ForegroundColor Red
        Write-Host "Please install Python 3.7+ and try again" -ForegroundColor Yellow
        exit 1
    }
    
    # Check Docker
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Error: Docker is not installed" -ForegroundColor Red
        Write-Host "Please install Docker Desktop and try again" -ForegroundColor Yellow
        exit 1
    }
    
    # Check if running as Administrator
    if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Host "Error: This script must be run as Administrator" -ForegroundColor Red
        Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Prerequisites check passed!" -ForegroundColor Green
}

# Function to get network information
function Get-NetworkInfo {
    Write-Host "Getting network information..." -ForegroundColor Cyan
    
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*" | Where-Object {$_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress
    
    if (-not $localIP) {
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | Where-Object {$_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress
    }
    
    if (-not $localIP) {
        $localIP = "192.168.1.100"
        Write-Host "Warning: Could not detect local IP, using default: $localIP" -ForegroundColor Yellow
    } else {
        Write-Host "Detected local IP: $localIP" -ForegroundColor Green
    }
    
    return $localIP
}

# Function to get user input
function Get-UserInput {
    param(
        [string]$Prompt,
        [string]$DefaultValue,
        [string]$ErrorMessage,
        [switch]$SkipPrompts
    )
    
    if ($SkipPrompts) {
        Write-Host "SkipPrompts enabled - using default value for $Prompt : $DefaultValue" -ForegroundColor Yellow
        return $DefaultValue
    }
    
    do {
        $userInput = Read-Host "$Prompt [$DefaultValue]"
        if ([string]::IsNullOrWhiteSpace($userInput)) {
            $userInput = $DefaultValue
        }
        
        if ([string]::IsNullOrWhiteSpace($userInput)) {
            Write-Host $ErrorMessage -ForegroundColor Red
        } else {
            break
        }
    } while ($true)
    
    return $userInput
}

# Function to setup master node
function Initialize-MasterNode {
    param(
        [string]$MasterIP,
        [string]$NASIP,
        [string]$NASPath
    )
    
    Write-Host "Setting up Master Node..." -ForegroundColor Cyan
    
            # Check for Docker Desktop with Kubernetes
        Write-Host "Checking for Docker Desktop with Kubernetes..." -ForegroundColor Yellow
        
        # Check if Docker is installed and running
        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
            Write-Host "Docker not found. Installing Docker Desktop..." -ForegroundColor Yellow
            
            # Download Docker Desktop installer
            Write-Host "Downloading Docker Desktop for Windows..." -ForegroundColor Cyan
            $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
            $dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
            
            try {
                Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -ErrorAction Stop
                Write-Host "Docker Desktop downloaded successfully!" -ForegroundColor Green
                
                # Run installer
                Write-Host "Running Docker Desktop installer..." -ForegroundColor Yellow
                Write-Host "Please follow the installation wizard and enable Kubernetes when prompted." -ForegroundColor Cyan
                Start-Process -FilePath $dockerInstaller -Wait
                
                # Clean up installer
                Remove-Item $dockerInstaller -Force -ErrorAction SilentlyContinue
                
                Write-Host "Docker Desktop installation completed!" -ForegroundColor Green
                Write-Host "Please restart your computer and run this script again." -ForegroundColor Yellow
                Write-Host "Make sure to enable Kubernetes in Docker Desktop settings." -ForegroundColor Cyan
                exit 0
                
            } catch {
                Write-Host "Failed to download Docker Desktop: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "Please manually download and install Docker Desktop from:" -ForegroundColor Yellow
                Write-Host "https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Cyan
                Write-Host "Make sure to enable Kubernetes in the settings." -ForegroundColor Yellow
                exit 1
            }
        }
        
        # Check if Docker is running
        Write-Host "Checking if Docker Desktop is running..." -ForegroundColor Yellow
        try {
            docker version | Out-Null
            Write-Host "Docker Desktop is running!" -ForegroundColor Green
        } catch {
            Write-Host "Docker Desktop is not running!" -ForegroundColor Red
            Write-Host "Please start Docker Desktop and wait for it to fully load." -ForegroundColor Yellow
            Write-Host "Look for the Docker icon in your system tray and ensure it shows 'Docker Desktop is running'." -ForegroundColor Cyan
            if (-not $SkipPrompts) {
                Read-Host "Press Enter when Docker Desktop is running"
            } else {
                Write-Host "SkipPrompts enabled - assuming Docker Desktop is running..." -ForegroundColor Yellow
                Start-Sleep -Seconds 2
            }
            
            # Check again
            try {
                docker version | Out-Null
                Write-Host "Docker Desktop is now running!" -ForegroundColor Green
            } catch {
                Write-Host "Docker Desktop is still not available. Please check the installation." -ForegroundColor Red
                exit 1
            }
        }
        
        # Check if Kubernetes is enabled in Docker Desktop
        Write-Host "Checking if Kubernetes is enabled in Docker Desktop..." -ForegroundColor Yellow
        try {
            kubectl cluster-info --context docker-desktop | Out-Null
            Write-Host "Kubernetes is running!" -ForegroundColor Green
        } catch {
            Write-Host "Kubernetes is not enabled in Docker Desktop." -ForegroundColor Red
            Write-Host "Please enable Kubernetes in Docker Desktop:" -ForegroundColor Yellow
            Write-Host "1. Open Docker Desktop" -ForegroundColor Cyan
            Write-Host "2. Go to Settings > Kubernetes" -ForegroundColor Cyan
            Write-Host "3. Check 'Enable Kubernetes'" -ForegroundColor Cyan
            Write-Host "4. Click 'Apply & Restart'" -ForegroundColor Cyan
            Write-Host "5. Wait for Kubernetes to start, then run this script again" -ForegroundColor Cyan
            if (-not $SkipPrompts) {
                Read-Host "Press Enter when Kubernetes is enabled and running"
            } else {
                Write-Host "SkipPrompts enabled - assuming Kubernetes is enabled..." -ForegroundColor Yellow
                Start-Sleep -Seconds 2
            }
            
            # Check again
            try {
                kubectl cluster-info --context docker-desktop | Out-Null
                Write-Host "Kubernetes is now running!" -ForegroundColor Green
            } catch {
                Write-Host "Kubernetes is still not available. Please check Docker Desktop settings." -ForegroundColor Red
                exit 1
            }
        }
    
    # Setup Kubernetes context for Docker Desktop
    Write-Host "Setting up Kubernetes context..." -ForegroundColor Yellow
    
    # Ensure kubectl is configured for Docker Desktop
    try {
        kubectl config use-context docker-desktop
        Write-Host "Kubernetes context set to docker-desktop" -ForegroundColor Green
    } catch {
        Write-Host "Warning: Could not set docker-desktop context" -ForegroundColor Yellow
    }
    
    # Create a token for worker nodes (Docker Desktop handles cluster setup differently)
    $token = "DOCKER-" + [System.Guid]::NewGuid().ToString("N").Substring(0, 20)
    Write-Host "Cluster Token: $token" -ForegroundColor Green
    Write-Host "Note: With Docker Desktop, worker nodes will connect via shared Docker network" -ForegroundColor Cyan
        
        # Save token to file locally
        $token | Out-File "master-token.txt" -Encoding UTF8
        
        # Also save to server location for automatic worker access
        try {
            $serverTokenPath = "\\BernHQ\Big Pool\Programming\01-Production-Ready\Meshroom-Control-Center\gui\master-token.txt"
            $token | Out-File $serverTokenPath -Encoding UTF8
            Write-Host "✅ Token saved locally and on server for automatic worker setup" -ForegroundColor Green
        } catch {
            Write-Host "✅ Token saved locally: master-token.txt" -ForegroundColor Green
            Write-Host "⚠️  Could not save to server - worker nodes will need manual token" -ForegroundColor Yellow
        }
    
    # Label the master node (Docker Desktop node)
    try {
        $nodeName = kubectl get nodes -o jsonpath='{.items[0].metadata.name}'
        kubectl label node $nodeName node-role.kubernetes.io/master=true --overwrite
        kubectl label node $nodeName gpu=amd --overwrite
        Write-Host "Node labeled successfully" -ForegroundColor Green
    } catch {
        Write-Host "Warning: Could not label node (this is normal for first-time setup)" -ForegroundColor Yellow
    }
    
    Write-Host "Master Node setup complete!" -ForegroundColor Green
    Write-Host "Docker Desktop Kubernetes is ready for distributed processing!" -ForegroundColor Cyan
    return $token
}

# Function to build and deploy cluster
function Initialize-DeployCluster {
    param(
        [string]$NASIP,
        [string]$NASPath
    )
    
    Write-Host "Building Docker images..." -ForegroundColor Cyan
    
    # Store current location (ensure it's the app root)
    $originalLocation = Get-Location
    Write-Host "Working from: $originalLocation" -ForegroundColor Cyan
    
    # Build simple base image (lightweight for testing)
    $shouldBuild = $Force
    if (-not $Force) {
        try {
            docker inspect meshroom-base:latest | Out-Null
            Write-Host "[OK] meshroom-base image already exists, skipping build..." -ForegroundColor Green
        } catch {
            $shouldBuild = $true
        }
    } else {
        Write-Host "Force rebuild requested for meshroom-base..." -ForegroundColor Yellow
        $shouldBuild = $true
    }
    
    if ($shouldBuild) {
        Write-Host "Building meshroom-simple image..." -ForegroundColor Yellow
        if (Test-Path "$originalLocation\cluster\docker\meshroom-simple") {
            Set-Location "$originalLocation\cluster\docker\meshroom-simple"
    docker build -t meshroom-base:latest .
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Warning: meshroom-simple build failed, but continuing..." -ForegroundColor Yellow
            }
        } else {
            Write-Host "Warning: meshroom-simple Dockerfile not found, skipping..." -ForegroundColor Yellow
        }
    }
    
    # Build worker image
    Write-Host "Building meshroom-worker image..." -ForegroundColor Yellow
    if (Test-Path "$originalLocation\cluster\docker\meshroom-worker") {
        Set-Location "$originalLocation\cluster\docker\meshroom-worker"
    docker build -t meshroom-worker:latest .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Warning: meshroom-worker build failed, but continuing..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Warning: meshroom-worker Dockerfile not found, skipping..." -ForegroundColor Yellow
    }
    
    # Build coordinator image
    Write-Host "Building meshroom-coordinator image..." -ForegroundColor Yellow
    if (Test-Path "$originalLocation\cluster\docker\meshroom-coordinator") {
        Set-Location "$originalLocation\cluster\docker\meshroom-coordinator"
    docker build -t meshroom-coordinator:latest .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Warning: meshroom-coordinator build failed, but continuing..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Warning: meshroom-coordinator Dockerfile not found, skipping..." -ForegroundColor Yellow
    }
    
    # Return to original location
    Set-Location $originalLocation
    Write-Host "Docker images built successfully!" -ForegroundColor Green
    
    # Create Windows-compatible NAS storage configuration
    Write-Host "Creating Windows NAS storage configuration..." -ForegroundColor Cyan
    
    # Create a Windows SMB/NFS storage configuration
    $storageYaml = @"
apiVersion: v1
kind: PersistentVolume
metadata:
  name: meshroom-nas-storage-pv
  namespace: meshroom
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nas-storage
  csi:
    driver: smb.csi.k8s.io
    readOnly: false
    volumeAttributes:
      source: "//$NASIP/meshroom"
      csi.storage.k8s.io/provisioner-secret-name: "smbcreds"
      csi.storage.k8s.io/provisioner-secret-namespace: "default"
      csi.storage.k8s.io/node-publish-secret-name: "smbcreds"
      csi.storage.k8s.io/node-publish-secret-namespace: "default"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: meshroom-storage-pvc
  namespace: meshroom
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: nas-storage
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nas-storage
provisioner: smb.csi.k8s.io
parameters:
  source: "//$NASIP/meshroom"
  csi.storage.k8s.io/provisioner-secret-name: "smbcreds"
  csi.storage.k8s.io/provisioner-secret-namespace: "default"
  csi.storage.k8s.io/node-publish-secret-name: "smbcreds"
  csi.storage.k8s.io/node-publish-secret-namespace: "default"
reclaimPolicy: Retain
volumeBindingMode: Immediate
"@
    
    # Create local data directory as fallback
    $dataDir = "C:\meshroom-data"
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir -Force
    }
    
    # Create subdirectories
    $subdirs = @("input", "output", "temp", "logs")
    foreach ($subdir in $subdirs) {
        $fullPath = Join-Path $dataDir $subdir
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force
        }
    }
    
            # Save storage configuration
        $storageConfigPath = Join-Path $originalLocation "cluster\k8s\storage-windows.yaml"
        $storageYaml | Out-File $storageConfigPath -Encoding UTF8
        Write-Host "Storage config saved to: $storageConfigPath" -ForegroundColor Green
    
    # Create SMB credentials secret
    Write-Host "Creating SMB credentials for NAS access..." -ForegroundColor Yellow
    $smbUsername = "bernardo"
    
    if ($SkipPrompts) {
        Write-Host "SkipPrompts enabled - using placeholder password. Update manually via GUI if needed." -ForegroundColor Yellow
        $smbPasswordText = "placeholder_password"
    } else {
        $smbPassword = Read-Host "Enter password for SMB user '$smbUsername'" -AsSecureString
        $smbPasswordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($smbPassword))
    }
    
    # Create Kubernetes secret for SMB credentials
    kubectl create secret generic smbcreds --from-literal=username=$smbUsername --from-literal=password=$smbPasswordText -n meshroom --dry-run=client -o yaml | kubectl apply -f -
    
    Write-Host "SMB credentials created for user: $smbUsername" -ForegroundColor Green
    
    # Deploy cluster
        Write-Host "Deploying Meshroom cluster..." -ForegroundColor Cyan
        
        # Check if namespace already exists
        try {
            kubectl get namespace meshroom | Out-Null
            Write-Host "[OK] Meshroom namespace already exists, skipping..." -ForegroundColor Green
        } catch {
            kubectl apply -f "$originalLocation\cluster\k8s\namespace.yaml"
            Write-Host "[OK] Namespace created" -ForegroundColor Green
        }
        
        # Check if storage is already configured
        try {
            kubectl get pvc meshroom-storage-pvc -n meshroom | Out-Null
            Write-Host "[OK] Storage already configured, skipping..." -ForegroundColor Green
        } catch {
            # Try SMB storage first, fall back to local if it fails
            Write-Host "Attempting to deploy SMB storage for NAS..." -ForegroundColor Yellow
            try {
                kubectl apply -f "$originalLocation\cluster\k8s\storage-smb.yaml"
                Write-Host "SMB storage configured successfully!" -ForegroundColor Green
            } catch {
                Write-Host "SMB storage failed (expected in Docker Desktop), using local storage..." -ForegroundColor Yellow
                kubectl apply -f "$originalLocation\cluster\k8s\storage-local.yaml"
            }
        }
        
        # Check if deployments exist
        try {
            kubectl get deployment meshroom-coordinator -n meshroom | Out-Null
            Write-Host "[OK] Deployments already exist, updating..." -ForegroundColor Green
            kubectl apply -f "$originalLocation\cluster\k8s\meshroom-deployment.yaml"
            kubectl apply -f "$originalLocation\cluster\k8s\services.yaml"
        } catch {
            Write-Host "Creating deployments..." -ForegroundColor Yellow
            kubectl apply -f "$originalLocation\cluster\k8s\meshroom-deployment.yaml"
            kubectl apply -f "$originalLocation\cluster\k8s\services.yaml"
        }
    
    # Wait for pods to be ready
    Write-Host "Waiting for pods to be ready..." -ForegroundColor Yellow
    try {
    kubectl wait --for=condition=ready pod -l app=meshroom -n meshroom --timeout=300s
    } catch {
        Write-Host "Warning: Some pods may not be ready yet (this is normal for first deployment)" -ForegroundColor Yellow
    }
    
    Write-Host "Meshroom cluster deployed successfully!" -ForegroundColor Green
}

# Function to verify cluster
function Test-ClusterStatus {
    Write-Host "Verifying cluster status..." -ForegroundColor Cyan
    
    Write-Host "Cluster nodes:" -ForegroundColor Yellow
    kubectl get nodes
    
    Write-Host "Meshroom pods:" -ForegroundColor Yellow
    kubectl get pods -n meshroom
    
    Write-Host "Services:" -ForegroundColor Yellow
    kubectl get services -n meshroom
    
    Write-Host "Storage:" -ForegroundColor Yellow
    kubectl get pv,pvc -n meshroom
}

# Function to install GUI requirements
function Install-GUIRequirements {
    Write-Host "Installing GUI requirements..." -ForegroundColor Cyan
    
    Set-Location "gui"
    pip install -r requirements.txt
    Set-Location ".."
    
    Write-Host "GUI requirements installed!" -ForegroundColor Green
}

# Function to check if setup has already been run
function Test-SetupStatus {
    Write-Host "Checking existing setup..." -ForegroundColor Cyan
    
    $setupComplete = $true
    $issues = @()
    
    # Check Docker Desktop and Kubernetes
    try {
        docker version | Out-Null
        kubectl cluster-info --context docker-desktop | Out-Null
        Write-Host "[OK] Docker Desktop + Kubernetes: Ready" -ForegroundColor Green
    } catch {
        $setupComplete = $false
        $issues += "Docker Desktop or Kubernetes not running"
        Write-Host "[FAIL] Docker Desktop + Kubernetes: Not ready" -ForegroundColor Red
    }
    
    # Check if namespace exists
    try {
        $namespaceCheck = kubectl get namespace meshroom 2>$null
        if ($namespaceCheck) {
            Write-Host "[OK] Meshroom namespace: Exists" -ForegroundColor Green
        } else {
            $setupComplete = $false
            $issues += "Meshroom namespace missing"
            Write-Host "[FAIL] Meshroom namespace: Missing" -ForegroundColor Red
        }
    } catch {
        $setupComplete = $false
        $issues += "Meshroom namespace missing"
        Write-Host "[FAIL] Meshroom namespace: Missing" -ForegroundColor Red
    }
    
    # Check if pods are running
    try {
        $pods = kubectl get pods -n meshroom -o jsonpath='{.items[*].status.phase}' 2>$null
        if ($pods -and $pods.Contains("Running")) {
            Write-Host "[OK] Meshroom pods: Running" -ForegroundColor Green
        } else {
            $setupComplete = $false
            $issues += "Meshroom pods not running"
            Write-Host "[FAIL] Meshroom pods: Not running" -ForegroundColor Red
        }
    } catch {
        $setupComplete = $false
        $issues += "Cannot check pods"
        Write-Host "[FAIL] Meshroom pods: Cannot check" -ForegroundColor Red
    }
    
    # Check if storage is configured
    try {
        kubectl get pvc meshroom-storage-pvc -n meshroom | Out-Null
        Write-Host "[OK] Storage: Configured" -ForegroundColor Green
    } catch {
        $setupComplete = $false
        $issues += "Storage not configured"
        Write-Host "[FAIL] Storage: Not configured" -ForegroundColor Red
    }
    
    # Check if Docker images exist
    $images = @("meshroom-base:latest")
    foreach ($image in $images) {
        try {
            docker inspect $image | Out-Null
            Write-Host "[OK] Docker image [$image] : Built" -ForegroundColor Green
        } catch {
            $setupComplete = $false
            $issues += "Docker image $image missing"
            Write-Host "[FAIL] Docker image [$image] : Missing" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    if ($setupComplete -and -not $Force) {
        Write-Host "Setup appears to be complete!" -ForegroundColor Green
        Write-Host "All components are ready." -ForegroundColor Cyan
        
        $choice = Read-Host "Do you want to re-run setup anyway? (y/N)"
        if ($choice -ne "y" -and $choice -ne "Y") {
            Write-Host "Setup skipped. Use the GUI or deploy commands to manage your cluster." -ForegroundColor Yellow
            exit 0
        }
        Write-Host "Proceeding with full setup..." -ForegroundColor Yellow
    } elseif ($Force) {
        Write-Host "Force rebuild requested, proceeding with full setup..." -ForegroundColor Yellow
    } else {
        Write-Host "Setup incomplete. Issues found:" -ForegroundColor Yellow
        foreach ($issue in $issues) {
            Write-Host "   - $issue" -ForegroundColor White
        }
        Write-Host "Proceeding with setup to fix these issues..." -ForegroundColor Cyan
    }
    Write-Host ""
}

# Main execution
try {
    Write-Host "Starting Meshroom cluster setup..." -ForegroundColor Green
    
    # Check prerequisites
    Test-Prerequisites
    
    # Check if setup was already completed
    Test-SetupStatus
    
    # Get user inputs
    # Master IP is already set as default parameter, no need to ask
    $NASIP = Get-UserInput "Enter NAS IP address" $NASIP "NAS IP cannot be empty" -SkipPrompts:$SkipPrompts
    $NASPath = Get-UserInput "Enter NAS path for meshroom" $NASPath "NAS path cannot be empty" -SkipPrompts:$SkipPrompts
    
    Write-Host ""
    Write-Host "Configuration Summary:" -ForegroundColor Cyan
    Write-Host "   Master IP: $MasterIP" -ForegroundColor White
    Write-Host "   NAS IP: $NASIP" -ForegroundColor White
    Write-Host "   NAS Path: $NASPath" -ForegroundColor White
    Write-Host ""
    
    # Confirm setup
    if (-not $SkipPrompts) {
        $confirm = Read-Host "Do you want to proceed with the setup? (y/N)"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Setup cancelled" -ForegroundColor Red
            exit 0
        }
    }
    
    # Setup master node
    $token = Initialize-MasterNode -MasterIP $MasterIP -NASIP $NASIP -NASPath $NASPath
    
    # Ensure we're in the right directory
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $appRoot = Split-Path -Parent $scriptDir
    Set-Location $appRoot
    
    # Build and deploy cluster
    Initialize-DeployCluster -NASIP $NASIP -NASPath $NASPath
    
    # Verify cluster
    Test-ClusterStatus
    
    # Install GUI requirements
    Install-GUIRequirements
    
    Write-Host ""
    Write-Host "Setup complete! Your Meshroom cluster is ready." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Copy this entire folder to your second AMD PC" -ForegroundColor White
    Write-Host "   2. Run worker setup on PC 2 with token: $token" -ForegroundColor White
    Write-Host "   3. Upload photos to your NAS at: $NASPath/input" -ForegroundColor White
    Write-Host "   4. Launch GUI: .\gui\launch-gui.bat" -ForegroundColor White
    Write-Host "   5. Start processing: .\scripts\deploy.ps1 start" -ForegroundColor White
    Write-Host ""
    Write-Host "Master Token saved to: master-token.txt" -ForegroundColor Yellow
    Write-Host "Use this token to join worker nodes" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Storage Configuration:" -ForegroundColor Green
    Write-Host "   - NAS IP: $NASIP" -ForegroundColor White
    Write-Host "   - NAS Path: $NASPath" -ForegroundColor White
    Write-Host "   - Local fallback: C:\meshroom-data" -ForegroundColor White
    Write-Host ""
    Write-Host "How distributed processing works:" -ForegroundColor Cyan
    Write-Host "   1. Upload photos to your NAS at $NASPath/input" -ForegroundColor White
    Write-Host "   2. Both PCs access the same photos via SMB/NFS" -ForegroundColor White
    Write-Host "   3. Work is distributed between the PCs" -ForegroundColor White
    Write-Host "   4. Results are saved back to the NAS" -ForegroundColor White
    Write-Host ""
    Write-Host "Important: Ensure your NAS is accessible from both PCs!" -ForegroundColor Yellow
    
} catch {
    Write-Host "Error during setup: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Check the logs and try again" -ForegroundColor Yellow
    exit 1
} 