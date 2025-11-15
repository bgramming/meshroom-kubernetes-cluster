# 🎯 Meshroom Kubernetes Cluster Monitor - GUI

A user-friendly graphical interface for monitoring and managing your distributed Meshroom cluster.

## 🚀 Quick Start

### Windows (Easiest)
1. **Double-click** `launch-gui.bat`
2. The GUI will start automatically

### PowerShell
```powershell
.\launch-gui.ps1
```

### Python (Manual)
```bash
pip install -r requirements.txt
python meshroom-monitor.py
```

## 🖥️ GUI Features

### 📊 **Dashboard Tab**
- **Cluster Status**: Overall health and status
- **Workflow Status**: Current processing status
- **Quick Actions**: Start/stop workflows, refresh status

### 🏗️ **Cluster Tab**
- **Nodes**: View all cluster nodes (PCs)
- **Pods**: Monitor running containers
- **Services**: Check network services
- **Storage**: View persistent volumes

### 🔄 **Workflows Tab**
- **Active Workflows**: See running photogrammetry jobs
- **Workflow History**: View completed/failed jobs
- **Progress Tracking**: Real-time status updates
- **Workflow Management**: Start, stop, pause workflows

### 📝 **Logs Tab**
- **Real-time Logs**: Live log streaming
- **Log Filtering**: Search and filter logs
- **Log Export**: Save logs to files
- **Error Highlighting**: Easy error identification

### ⚙️ **Configuration Tab**
- **Cluster Settings**: Modify cluster parameters
- **Workflow Settings**: Adjust processing parameters
- **UI Preferences**: Customize interface
- **Advanced Options**: Expert-level configurations

## 🎮 **Control Buttons**

| Button | Action | Description |
|--------|--------|-------------|
| 🔄 **Refresh Status** | Updates all cluster information |
| 🚀 **Start Workflow** | Launches photogrammetry processing |
| ⏹️ **Stop Workflows** | Stops all running workflows |
| 🧹 **Cleanup Cluster** | Removes cluster resources |
| 💾 **Save Logs** | Exports logs to files |
| ⚙️ **Settings** | Opens configuration panel |

## 📱 **Real-time Monitoring**

- **Auto-refresh**: Updates every 30 seconds
- **Status Indicators**: Color-coded health status
- **Progress Bars**: Visual workflow progress
- **Resource Usage**: CPU, memory, storage monitoring
- **Alert System**: Notifications for issues

## 🔧 **Configuration Options**

### Cluster Settings
- Namespace configuration
- Refresh intervals
- Log levels
- Auto-refresh toggle

### Workflow Settings
- Default workflow file
- Auto-start options
- Log saving preferences
- Output directories

### UI Preferences
- Theme selection (Dark/Light)
- Window size
- Language options
- Advanced mode toggle

## 📊 **Status Indicators**

| Status | Color | Meaning |
|--------|-------|---------|
| 🟢 **Ready** | Green | Everything working normally |
| 🟡 **Warning** | Yellow | Minor issues detected |
| 🔴 **Error** | Red | Critical problems |
| 🔵 **Processing** | Blue | Workflow in progress |
| ⚫ **Unknown** | Gray | Status unclear |

## 🚨 **Alert System**

The GUI automatically detects and alerts you to:
- **Workflow failures**
- **High resource usage**
- **Pod restarts**
- **Storage issues**
- **Network problems**

## 💾 **Data Export**

- **Log Files**: Save logs in text format
- **Status Reports**: Export cluster status
- **Configuration**: Save/load settings
- **Workflow History**: Export job history

## 🔍 **Troubleshooting**

### GUI Won't Start
1. Check Python installation: `python --version`
2. Install requirements: `pip install -r requirements.txt`
3. Verify kubectl: `kubectl version --client`

### No Cluster Data
1. Ensure cluster is running
2. Check kubectl configuration
3. Verify namespace exists: `kubectl get ns meshroom`

### Performance Issues
1. Reduce refresh interval
2. Disable auto-refresh
3. Close unnecessary tabs

## 📁 **File Structure**

```
gui/
├── 📱 meshroom-monitor.py      # Main GUI application
├── 📋 requirements.txt          # Python dependencies
├── 🚀 launch-gui.bat           # Windows launcher
├── 🔧 launch-gui.ps1           # PowerShell launcher
├── ⚙️ config.json              # GUI configuration
└── 📚 README.md                # This file
```

## 🎯 **Use Cases**

### **For Beginners**
- Easy cluster monitoring
- One-click workflow management
- Visual status indicators
- Simple configuration

### **For Power Users**
- Advanced cluster management
- Detailed resource monitoring
- Custom workflow configurations
- Log analysis tools

### **For Teams**
- Shared cluster monitoring
- Workflow collaboration
- Centralized logging
- Status reporting

## 🔮 **Future Features**

- [ ] **Web Interface**: Browser-based access
- [ ] **Mobile App**: Phone/tablet monitoring
- [ ] **Email Alerts**: Notification system
- [ ] **API Integration**: External tool support
- [ ] **Custom Dashboards**: Personalized views
- [ ] **Performance Analytics**: Historical data

## 🆘 **Getting Help**

1. **Check the logs** in the GUI
2. **Verify cluster status** with kubectl
3. **Review configuration** in config.json
4. **Check troubleshooting** section above

## 🎉 **You're Ready!**

Your Meshroom cluster now has a professional, user-friendly monitoring interface! 

**Happy Monitoring! 🎯📊** 