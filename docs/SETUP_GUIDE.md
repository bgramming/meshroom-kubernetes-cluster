# Meshroom Kubernetes Cluster - Complete Setup Guide

This guide will walk you through setting up a distributed Meshroom cluster across your two AMD PCs using Kubernetes and Docker.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] 2 AMD-based PCs with Windows 10/11
- [ ] At least 16GB RAM per PC
- [ ] AMD GPU with ROCm support (recommended)
- [ ] Synology NAS with NFS enabled
- [ ] Gigabit network connection between PCs
- [ ] Administrator access on both PCs
- [ ] At least 100GB free space on each PC

## 🏗️ Architecture Overview

```
[Your Photos] → [Synology NAS] → [Kubernetes Cluster] → [Distributed Processing]
                                                           ↓
                    ┌─────────────────┬─────────────────┐
                    │   AMD PC 1      │   AMD PC 2      │
                    │ (Master Node)   │ (Worker Node)   │
                    │                 │                 │
                    │ • Feature       │ • Feature       │
                    │   Extraction   │   Extraction    │
                    │ • Depth Maps   │ • Depth Maps    │
                    │ • Meshing      │ • Texturing     │
                    └─────────────────┴─────────────────┘
```

## 🚀 Step 1: Prepare Your Synology NAS

### 1.1 Enable NFS Service
1. Open **DSM** (Synology DiskStation Manager)
2. Go to **Control Panel** → **File Services**
3. Click **NFS** tab
4. Check **Enable NFS service**
5. Click **Apply**

### 1.2 Create Shared Folder
1. Go to **File Station**
2. Create a new folder called `meshroom`
3. Right-click the folder → **Properties**
4. Go to **NFS Permissions** tab
5. Click **Create**
6. Set permissions:
   - **Hostname or IP**: `*` (allows all hosts)
   - **Privilege**: `Read/Write`
   - **Squash**: `No mapping`
   - **Security**: `sys`
7. Click **OK**

### 1.3 Note Your NAS Details
- **NAS IP Address**: (e.g., 192.168.1.100)
- **NFS Path**: `/volume1/meshroom`
- **Network Subnet**: (e.g., 192.168.1.0/24)

## 🖥️ Step 2: Setup PC 1 (Master Node)

### 2.1 Download and Extract
1. Download this project to `C:\meshroom-kubernetes-cluster`
2. Open **PowerShell as Administrator**
3. Navigate to the project directory:
   ```powershell
   cd C:\meshroom-kubernetes-cluster
   ```

### 2.2 Run Master Setup
```powershell
.\scripts\setup-cluster.ps1 -IsMaster -MasterIP "YOUR_PC1_IP" -NASIP "YOUR_NAS_IP" -NASPath "/volume1/meshroom"
```

**Example:**
```powershell
.\scripts\setup-cluster.ps1 -IsMaster -MasterIP "192.168.1.50" -NASIP "192.168.1.100" -NASPath "/volume1/meshroom"
```

### 2.3 Note the Token
The script will output a **Master Node Token**. **Save this token** - you'll need it for PC 2.

**Example output:**
```
🔑 Master Node Token: K10a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
📝 Use this token to join worker nodes
```

## 🖥️ Step 3: Setup PC 2 (Worker Node)

### 3.1 Download and Extract
1. Download this project to `C:\meshroom-kubernetes-cluster`
2. Open **PowerShell as Administrator**
3. Navigate to the project directory:
   ```powershell
   cd C:\meshroom-kubernetes-cluster
   ```

### 3.2 Run Worker Setup
```powershell
.\scripts\setup-cluster.ps1 -IsWorker -MasterIP "PC1_IP" -WorkerToken "TOKEN_FROM_STEP_2" -NASIP "YOUR_NAS_IP" -NASPath "/volume1/meshroom"
```

**Example:**
```powershell
.\scripts\setup-cluster.ps1 -IsWorker -MasterIP "192.168.1.50" -WorkerToken "K10a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6" -NASIP "192.168.1.100" -NASPath "/volume1/meshroom"
```

## 🔍 Step 4: Verify Cluster Setup

### 4.1 Check Cluster Status (on PC 1)
```powershell
# Check nodes
kubectl get nodes

# Check pods
kubectl get pods -A

# Check services
kubectl get services -n meshroom

# Check storage
kubectl get pv,pvc -n meshroom
```

**Expected output:**
```
NAME        STATUS   ROLES    AGE   VERSION
amd-pc1     Ready    master   5m    v1.25.0+k3s1
amd-pc2     Ready    worker   3m    v1.25.0+k3s1

NAME                                    READY   STATUS    RESTARTS   AGE
meshroom-coordinator-7d8f9b4c5-abc12   1/1     Running   0          2m
meshroom-worker-6e9f8c3d2-def34        1/1     Running   0          2m
meshroom-worker-6e9f8c3d2-ghi56        1/1     Running   0          2m
meshroom-redis-8f7e6d5c4-jkl78         1/1     Running   0          2m
```

## 📸 Step 5: Upload Your Photos

### 5.1 Create Input Directory
On your Synology NAS, create the input directory:
```
/volume1/meshroom/input/
```

### 5.2 Upload Photos
1. Copy your photos to the NAS input directory
2. Ensure photos are in common formats (JPG, PNG, TIFF)
3. Recommended: 50-200 photos per project
4. Photos should have good overlap (60-80%)

### 5.3 Verify Upload
```powershell
# Check if photos are accessible
kubectl exec -it meshroom-coordinator-xxx -n meshroom -- ls -la /data/input
```

## 🚀 Step 6: Start Photogrammetry Processing

### 6.1 Start the Workflow
```powershell
kubectl apply -f workflows/photogrammetry-workflow.yaml
```

### 6.2 Monitor Progress
```powershell
# Check workflow status
kubectl get workflows -n meshroom

# View workflow logs
kubectl logs -f -l app=meshroom-coordinator -n meshroom

# Check worker logs
kubectl logs -f -l app=meshroom-worker -n meshroom
```

### 6.3 Track Progress
The workflow will automatically:
1. **Split photos** between both PCs
2. **Extract features** in parallel
3. **Generate depth maps** on both PCs
4. **Merge results** for final processing
5. **Create mesh and textures**

## 📊 Step 7: Monitor and Optimize

### 7.1 Resource Monitoring
```powershell
# Check resource usage
kubectl top nodes
kubectl top pods -n meshroom

# Check GPU usage (if available)
kubectl exec -it meshroom-worker-xxx -n meshroom -- nvidia-smi
```

### 7.2 Performance Tuning
Edit `config/meshroom-settings.json` to adjust:
- **Quality settings** (high/medium/low)
- **GPU acceleration** parameters
- **Memory limits** per worker
- **Batch sizes** for processing

## 🎯 Expected Performance

| Photos | Single PC | Two PCs | Improvement |
|--------|-----------|---------|-------------|
| 50     | 1-2 hours | 30-45 min | 2-3x faster |
| 100    | 2-4 hours | 1-2 hours | 2-3x faster |
| 200    | 4-8 hours | 2-4 hours | 2-3x faster |

**With GPU acceleration**: Additional 30-50% speed improvement

## 🐛 Troubleshooting

### Common Issues

#### 1. Pods Not Starting
```powershell
# Check events
kubectl get events -n meshroom

# Check pod details
kubectl describe pod <pod-name> -n meshroom

# Check logs
kubectl logs <pod-name> -n meshroom
```

#### 2. Storage Access Errors
```powershell
# Check storage status
kubectl get pv,pvc -n meshroom

# Check NFS connectivity
kubectl exec -it meshroom-coordinator-xxx -n meshroom -- ping YOUR_NAS_IP
```

#### 3. GPU Not Detected
```powershell
# Check node labels
kubectl get nodes --show-labels

# Check GPU resources
kubectl describe node <node-name> | findstr -i gpu
```

### Debug Commands
```powershell
# Check cluster health
kubectl get componentstatuses

# Check node resources
kubectl describe nodes

# Check persistent volumes
kubectl get pv,pvc --all-namespaces
```

## 🔧 Advanced Configuration

### Customize Processing Parameters
Edit `workflows/photogrammetry-workflow.yaml`:
- Adjust resource limits
- Change node selectors
- Modify processing steps
- Add custom validation

### Scale the Cluster
```powershell
# Scale workers
kubectl scale deployment meshroom-worker -n meshroom --replicas=4

# Add more nodes
# Follow Step 3 for additional PCs
```

### Backup and Restore
```powershell
# Backup workflow
kubectl get workflow meshroom-photogrammetry -n meshroom -o yaml > backup.yaml

# Restore workflow
kubectl apply -f backup.yaml
```

## 📚 Next Steps

1. **Process your first project** with the default settings
2. **Experiment with quality settings** to find the right balance
3. **Monitor performance** and adjust resource allocation
4. **Scale up** by adding more worker nodes if needed
5. **Automate workflows** for batch processing

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** using the commands above
2. **Verify network connectivity** between PCs and NAS
3. **Ensure sufficient resources** (RAM, CPU, storage)
4. **Check firewall settings** on both PCs
5. **Verify NFS permissions** on your Synology NAS

## 🎉 Congratulations!

You now have a distributed Meshroom cluster that can process photogrammetry projects across multiple AMD PCs simultaneously! 

**Happy 3D Scanning! 🎯📸** 