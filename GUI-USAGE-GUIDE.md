# 🎯 Meshroom Control Center - GUI Usage Guide

## ✅ No More CLI Prompts!

Your Meshroom system is now **100% GUI-driven** with zero command-line interaction required.

## 🚀 Quick Start

### Launch the GUI
```batch
# Any of these will work:
Meshroom.bat                    # Simple launch
Meshroom-Control-Center.bat     # Full featured  
launch-meshroom-admin.bat       # With admin privileges
```

### First Time Setup Workflow

1. **Launch GUI** → Click any .bat file
2. **Dashboard Tab** → Check system status
3. **Setup Tab** → Configure your network settings:
   - Master IP: Your main PC's IP
   - NAS IP: Your NAS device IP
   - NAS Path: UNC path to Meshroom folder
   - NAS Username: Your NAS login

4. **Setup Master Node**:
   - Click "Setup Master Node (Full)" 
   - Choose "No" for quick setup or "Yes" for force rebuild
   - All prompts handled via GUI dialogs

5. **Setup NAS Credentials**:
   - Click "Update NAS Credentials"
   - Enter password in secure GUI dialog

6. **Deploy Meshroom**:
   - Click "Deploy Meshroom Pods"
   - Confirm deployment prerequisites
   - Watch progress in Monitoring tab

## 📊 Dashboard Features

### Status Indicators
- 🟢 **Green** = Working properly
- 🟡 **Orange** = Warning/Not configured  
- 🔴 **Red** = Error/Not working

### Quick Actions (All 9 CLI Options)
1. **Setup Master Node** → Configures main PC
2. **Setup Worker Node** → Adds additional PCs
3. **Check Cluster Status** → Real-time monitoring
4. **Demo Mode** → Test interface
5. **Mount NAS Storage** → Storage access
6. **Start Workflow** → Begin processing
7. **View Documentation** → Help files
8. **System Tools** → Settings access
9. **Exit Application** → Clean shutdown

## 🛠️ Tab Functions

### Dashboard Tab
- **Quick Actions** → All 9 CLI functions as buttons
- **System Status** → Real-time health indicators
- **Integrated Terminal** → Live logs + command execution
- **Quick Command Buttons** → Common kubectl/docker commands
- **Command History** → Use ↑/↓ arrows in terminal

### Setup Tab
- **Network Configuration** → IP addresses, paths
- **Setup Master Node (Full)** → Complete setup
- **Deploy Meshroom Pods** → Install processing pods
- **Update NAS Credentials** → Secure password update
- **Download Dependencies** → Get Docker images
- **Reset Cluster** → Clean restart

### Storage Tab
- **File Browser** → NAS access
- **Photo Upload** → Drag & drop images
- **Input/Output Folders** → Direct access

### Workflows Tab
- **Start Processing** → Begin photogrammetry
- **Stop Workflows** → Halt processing
- **View Results** → Access outputs

### Settings Tab
- **Claude Agent** → AI assistant controls
- **System Tools** → Terminal, Docker access
- **Export Config** → Save settings

## 🔧 Troubleshooting

### If Status Shows "Not Deployed"
1. Go to **Setup Tab**
2. Click **"Deploy Meshroom Pods"**
3. Monitor progress in **Dashboard Terminal**

### If NAS Issues
1. **Setup Tab** → **"Update NAS Credentials"**
2. Enter correct password in GUI dialog
3. Check network connectivity

### If Setup Stalls
- All prompts now handled via GUI
- No CLI interaction required
- Check **Dashboard Terminal** for detailed logs

## 🎯 Key Benefits

✅ **Point & Click** → No command typing
✅ **Visual Status** → See everything at a glance  
✅ **Secure Dialogs** → Password protection
✅ **Real-time Logs** → Live feedback
✅ **Auto-refresh** → Current information
✅ **Error Handling** → Clear status messages

**Your distributed 3D processing is now completely visual!** 🚀
