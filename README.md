# 🎯 Meshroom Control Center v2.0

**Distributed 3D Photogrammetry Processing System**  
Complete GUI-driven Kubernetes cluster management for multi-PC 3D reconstruction workflows.

## 🚀 Quick Start

### From Server (Recommended)
1. **Deploy to Server**: Run `deploy-to-server.ps1`
2. **Create Shortcuts**: Run `create-shortcuts.ps1` on each PC
3. **Launch**: Double-click desktop shortcut

### Local Development
1. **Launch GUI**: `launchers\Meshroom.bat`
2. **Admin Mode**: `launchers\launch-meshroom-admin.bat`

## 📁 Project Structure

```
Meshroom-Control-Center/
├── 📱 gui/                     # Main GUI application
├── 🔧 scripts/                 # PowerShell automation scripts  
├── 🐳 cluster/                 # Kubernetes & Docker configs
├── 📚 docs/                    # Documentation
├── 🤖 ai/                      # Claude AI Agent
├── 📄 launchers/               # Application entry points
└── 📋 logs/                    # System logs
```

## ✨ Features

### 🎯 Dashboard
- **Quick Actions** → All setup functions as buttons
- **Live Terminal** → Integrated CLI with command execution
- **System Status** → Real-time health monitoring
- **Quick Commands** → kubectl, docker shortcuts

### ⚙️ Setup & Management
- **Smart Setup** → Automated master/worker configuration
- **Pod Deployment** → One-click Kubernetes deployment
- **NAS Integration** → Secure credential management
- **Multi-PC Support** → Distributed processing setup

### 🔧 Advanced Features
- **Command History** → Terminal with ↑/↓ navigation
- **Log Export** → Save all operations to file
- **Auto-Updates** → Git-based synchronization
- **Error Handling** → Clear status indicators

## 🖥️ Multi-System Deployment

### Server Setup
```powershell
# Deploy to server
.\deploy-to-server.ps1 -InitGit

# Map network drives on each PC
.\create-shortcuts.ps1
```

### System Roles
- **Master PC (10.0.0.226)** → Kubernetes control plane + processing
- **Worker PC** → Additional processing nodes
- **NAS (10.0.0.80)** → Shared storage for photos/results

## 🔄 Version Control

### Git Workflow
```bash
# Development
git checkout -b feature/new-feature
git commit -m "Add new feature"

# Release
git checkout main
git merge feature/new-feature
git tag v2.0.0
```

### Automatic Updates
Both PCs automatically sync changes when connected to server deployment.

## 📋 Requirements

### Software
- **Python 3.7+** with tkinter
- **Docker Desktop** with Kubernetes enabled
- **PowerShell 5.1+**
- **Windows 10+**

### Hardware
- **Master PC**: 16GB+ RAM, SSD storage
- **Worker PC**: 8GB+ RAM, network access
- **NAS**: SMB share with read/write access

### Network
- **All PCs**: Same network subnet
- **NAS Access**: SMB/CIFS protocol
- **Internet**: For Docker image downloads

## 🎯 Usage

### First Time Setup
1. **Launch GUI** → Use desktop shortcut
2. **Configure Network** → Setup tab → Enter IPs
3. **Setup Master** → Click "Setup Master Node (Smart)"
4. **Deploy Pods** → Click "Deploy Meshroom Pods"
5. **Add Workers** → Run on other PCs with worker setup

### Daily Operation
1. **Upload Photos** → Storage tab → Upload to input folder
2. **Start Processing** → Workflows tab → Start photogrammetry
3. **Monitor Progress** → Dashboard terminal shows live updates
4. **Download Results** → Storage tab → Browse output folder

## 🔧 Troubleshooting

### Common Issues
- **No GUI Response** → Check terminal output in dashboard
- **Pods Not Starting** → Use "Test Connection" button
- **NAS Access Issues** → Update credentials in Setup tab
- **Network Problems** → Verify IP addresses in configuration

### Support Commands
```bash
# In dashboard terminal
kubectl get pods -n meshroom     # Check pod status
kubectl get nodes               # Check cluster nodes
docker ps                       # Running containers
kubectl logs -n meshroom <pod>  # Pod logs
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** → Complete installation instructions
- **[GUI Usage](GUI-USAGE-GUIDE.md)** → Interface walkthrough
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** → Server setup instructions

## 🤖 AI Assistant

**Claude Agent** provides intelligent monitoring and troubleshooting:
- **Automatic Issue Detection** → Proactive problem identification
- **Smart Recommendations** → Context-aware solutions
- **System Optimization** → Performance tuning suggestions

## 🔐 Security

### Data Protection
- **Encrypted Credentials** → Secure NAS password storage
- **Network Isolation** → Kubernetes namespace separation
- **Access Control** → Role-based permissions

### Backup Strategy
- **Git Versioning** → All configuration changes tracked
- **Server Storage** → Centralized file management
- **Log Retention** → Comprehensive audit trail

## 🎯 Roadmap

### v2.1 (Planned)
- [ ] Web-based monitoring interface
- [ ] Mobile app for remote monitoring
- [ ] Advanced workflow templates
- [ ] Cloud backup integration

### v2.2 (Future)
- [ ] Multi-cluster support
- [ ] Enhanced AI capabilities
- [ ] Performance analytics dashboard
- [ ] Automated scaling

## 🤝 Contributing

### Development Setup
1. Clone from server deployment
2. Create feature branch
3. Test on local system
4. Submit for review

### Code Standards
- **PowerShell**: Follow best practices
- **Python**: PEP 8 compliance
- **Documentation**: Update all relevant files

---

**Ready for distributed 3D processing!** 🚀

*For support, check the docs or run the AI assistant with troubleshooting mode.*
