# Meshroom Kubernetes Cluster - Deployment Script
# Use this script to deploy and manage your Meshroom cluster

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("deploy", "start", "stop", "status", "logs", "cleanup")]
    [string]$Action = "status",
    
    [Parameter(Mandatory=$false)]
    [string]$WorkflowFile = "cluster/workflows/photogrammetry-workflow.yaml"
)

Write-Host "Meshroom Cluster Management" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

# Check if kubectl is available
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "kubectl not found. Please run the setup script first." -ForegroundColor Red
    exit 1
}

# Check if namespace exists
$namespaceExists = kubectl get namespace meshroom -o name 2>$null
if (-not $namespaceExists) {
    Write-Host "Meshroom namespace not found. Please run the setup script first." -ForegroundColor Red
    exit 1
}

switch ($Action) {
    "deploy" {
        Write-Host "Deploying Meshroom cluster..." -ForegroundColor Cyan
        
        # Apply all manifests
        kubectl apply -f cluster/k8s/namespace.yaml
        if (Test-Path "cluster/k8s/storage-windows.yaml") {
            kubectl apply -f cluster/k8s/storage-windows.yaml
        } else {
            kubectl apply -f cluster/k8s/storage.yaml
        }
        kubectl apply -f cluster/k8s/meshroom-deployment.yaml
        kubectl apply -f cluster/k8s/services.yaml
        
        Write-Host "Deployment complete!" -ForegroundColor Green
    }
    
    "start" {
        Write-Host "Starting photogrammetry workflow..." -ForegroundColor Cyan
        
        if (Test-Path $WorkflowFile) {
            kubectl apply -f $WorkflowFile
            Write-Host "Workflow started!" -ForegroundColor Green
            Write-Host "Monitor progress: kubectl get workflows -n meshroom" -ForegroundColor Yellow
        } else {
            Write-Host "Workflow file not found: $WorkflowFile" -ForegroundColor Red
        }
    }
    
    "stop" {
        Write-Host "Stopping workflows..." -ForegroundColor Cyan
        
        # Get running workflows
        $workflows = kubectl get workflows -n meshroom -o name 2>$null
        if ($workflows) {
            foreach ($workflow in $workflows) {
                kubectl delete $workflow -n meshroom
            }
            Write-Host "Workflows stopped!" -ForegroundColor Green
        } else {
            Write-Host "No workflows found" -ForegroundColor Gray
        }
    }
    
    "status" {
        Write-Host "Cluster Status:" -ForegroundColor Cyan
        Write-Host ""
        
        Write-Host "Namespaces:" -ForegroundColor Yellow
        kubectl get namespaces | findstr meshroom
        
        Write-Host ""
        Write-Host "Pods:" -ForegroundColor Yellow
        kubectl get pods -n meshroom
        
        Write-Host ""
        Write-Host "Services:" -ForegroundColor Yellow
        kubectl get services -n meshroom
        
        Write-Host ""
        Write-Host "Storage:" -ForegroundColor Yellow
        kubectl get pvc -n meshroom
    }
    
    "logs" {
        Write-Host "Recent logs:" -ForegroundColor Cyan
        kubectl logs -n meshroom --tail=50 -l app=meshroom
    }
    
    "cleanup" {
        Write-Host "Cleaning up Meshroom cluster..." -ForegroundColor Red
        $confirm = Read-Host "Are you sure? This will delete everything (y/N)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            kubectl delete namespace meshroom
            Write-Host "Cleanup complete!" -ForegroundColor Green
        } else {
            Write-Host "Cleanup cancelled" -ForegroundColor Yellow
        }
    }
    
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Write-Host "Available actions: deploy, start, stop, status, logs, cleanup" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Quick commands:" -ForegroundColor Cyan
Write-Host "   .\deploy.ps1 status    - Check cluster status" -ForegroundColor White
Write-Host "   .\deploy.ps1 start     - Start photogrammetry workflow" -ForegroundColor White
Write-Host "   .\deploy.ps1 logs      - View recent logs" -ForegroundColor White
Write-Host "   .\deploy.ps1 stop      - Stop running workflows" -ForegroundColor White
