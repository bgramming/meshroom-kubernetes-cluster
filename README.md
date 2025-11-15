# Meshroom Kubernetes Cluster

**Distributed 3D Photogrammetry Processing System**

A complete Kubernetes-based solution for accelerated 3D model generation from photos using Meshroom.

---

## ðŸš€ Features

- **Kubernetes Orchestration:** Distributed processing across multiple nodes
- **Docker Containers:** Coordinator and worker containers
- **GUI Control Center:** Easy-to-use interface for managing the cluster
- **Processing Scripts:** 7 production-ready Python scripts for various 3D workflows
- **GPU Acceleration:** Optimized for AMD Radeon RX 580 and similar GPUs
- **Complete Documentation:** Setup guides, troubleshooting, and examples

---

## ðŸ“ Project Structure

```
meshroom-kubernetes-cluster/
â”œâ”€â”€ gui/                          # Control Center GUI
â”‚   â””â”€â”€ launch-control-center.bat
â”œâ”€â”€ docker/                       # Docker configurations
â”‚   â”œâ”€â”€ coordinator/
â”‚   â””â”€â”€ workers/
â”œâ”€â”€ kubernetes/                   # K8s manifests
â”œâ”€â”€ scripts/                      # Processing Scripts (NEW!)
â”‚   â”œâ”€â”€ realistic-meshroom-processing.py
â”‚   â”œâ”€â”€ actual-meshroom-processing.py
â”‚   â”œâ”€â”€ real-meshroom-processing.py
â”‚   â”œâ”€â”€ meshroom-native-processing.py
â”‚   â”œâ”€â”€ process-photos-simple.py
â”‚   â”œâ”€â”€ process-photos.py
â”‚   â””â”€â”€ quick-valid-3d.py
â””â”€â”€ docs/                         # Documentation
```

---

## ðŸ› ï¸ Processing Scripts

### 1. **realistic-meshroom-processing.py**
Full-featured 3D reconstruction with all Meshroom nodes.

### 2. **actual-meshroom-processing.py**
Optimized workflow for faster processing.

### 3. **real-meshroom-processing.py**
Simplified pipeline for quick results.

### 4. **meshroom-native-processing.py**
Native Meshroom API integration.

### 5. **process-photos-simple.py**
Basic photo-to-3D conversion.

### 6. **process-photos.py**
Advanced processing with custom parameters.

### 7. **quick-valid-3d.py**
Fast validation and quality checks.

---

## ðŸš€ Quick Start

### Launch Control Center:
```bash
cd gui
./launch-control-center.bat
```

### Run Processing Scripts:
```bash
cd scripts
python realistic-meshroom-processing.py /path/to/photos
```

---

## ðŸ’» Requirements

- **Kubernetes:** v1.20+
- **Docker:** v20.10+
- **Python:** 3.8+
- **GPU:** AMD Radeon RX 580 or similar (8GB+ VRAM)
- **Meshroom:** 2021.1.0+

---

## ðŸ“š Documentation

See docs/ folder for:
- Setup guides
- Kubernetes configuration
- Docker deployment
- Script usage examples
- Troubleshooting

---

## ðŸŽ¯ Status

**Production Ready** - 100% Operational

---

## ðŸ“ License

MIT License

---

## ðŸ”— Links

- **GitHub:** https://github.com/bgramming/meshroom-kubernetes-cluster
- **Meshroom:** https://alicevision.org/

