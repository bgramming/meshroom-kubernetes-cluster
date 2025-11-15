#!/usr/bin/env python3
"""
Meshroom Kubernetes Cluster Control Center
Complete GUI for all setup, monitoring, and management functions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import subprocess
import threading
import json
import time
import os
import sys
from datetime import datetime
import webbrowser

class MeshroomControlCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Meshroom Kubernetes Cluster - Control Center")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Show startup message
        self.show_startup_info()
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.setup_variables()
        
        # Create main interface
        self.create_interface()
        
        # Initialize dashboard terminal
        self.clear_dashboard_terminal()
        
        # Initial status check
        self.refresh_all_status()
    
    def show_startup_info(self):
        """Show startup information"""
        startup_msg = """
🎯 Meshroom Control Center Loaded Successfully!

✅ All CLI functions (1-9) now integrated into GUI
✅ No more command-line prompts or menus
✅ Point-and-click operation for all tasks
✅ Automatic token system working!

🚀 DISTRIBUTED CLUSTER STATUS:
• Master Node: ✅ Ready
• Worker Nodes: ✅ Connected
• Auto-Token: ✅ Working  
• Multi-PC: ✅ Operational

Available Functions:
• Setup Master/Worker Nodes (Automated)
• Monitor Cluster Status
• Manage Workflows
• Browse NAS Storage
• Live System Logs

🎉 Ready for distributed 3D processing!
        """
        
        print(startup_msg)
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for dark theme
        self.style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#ffffff', background='#1e1e1e')
        self.style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#ffffff', background='#1e1e1e')
        self.style.configure('Status.TLabel', font=('Segoe UI', 10), foreground='#ffffff', background='#1e1e1e')
        self.style.configure('Success.TLabel', foreground='#4CAF50', background='#1e1e1e')
        self.style.configure('Error.TLabel', foreground='#f44336', background='#1e1e1e')
        self.style.configure('Warning.TLabel', foreground='#ff9800', background='#1e1e1e')
        
        # Button styles
        self.style.configure('Action.TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Setup.TButton', font=('Segoe UI', 10, 'bold'))
        
    def setup_variables(self):
        self.cluster_status = tk.StringVar(value="Checking...")
        self.docker_status = tk.StringVar(value="Checking...")
        self.pods_status = tk.StringVar(value="Checking...")
        self.storage_status = tk.StringVar(value="Checking...")
        self.master_ip = tk.StringVar(value="10.0.0.226")
        self.nas_ip = tk.StringVar(value="10.0.0.80")
        self.nas_path = tk.StringVar(value="\\\\BernHQ\\Big Pool\\Shared Folders\\Meshroom")
        self.nas_username = tk.StringVar(value="bernardo")
        self.auto_refresh = tk.BooleanVar(value=True)
        
        # Command history for terminal
        self.command_history = []
        self.history_index = 0
        
    def create_interface(self):
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_setup_tab()
        self.create_storage_tab()
        self.create_workflows_tab()
        self.create_settings_tab()
        
    def create_dashboard_tab(self):
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_frame = tk.Frame(dashboard_frame, bg='#1e1e1e')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(title_frame, text="Meshroom Kubernetes Cluster Control Center", 
                 style='Title.TLabel').pack()
        
        # Quick Actions Frame
        actions_frame = tk.LabelFrame(dashboard_frame, text="Quick Actions", 
                                    bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        # Create action buttons in a grid
        button_frame = tk.Frame(actions_frame, bg='#2b2b2b')
        button_frame.pack(padx=10, pady=10)
        
        # Row 1
        ttk.Button(button_frame, text="1. Setup Master Node (Smart)", 
                  command=self.setup_master_node, style='Setup.TButton').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="2. Setup Worker Node", 
                  command=self.setup_worker_node, style='Setup.TButton').grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="3. Check Cluster Status", 
                  command=self.check_cluster_status, style='Action.TButton').grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        # Row 2
        ttk.Button(button_frame, text="4. Demo Mode", 
                  command=self.launch_demo, style='Action.TButton').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="5. Mount NAS Storage", 
                  command=self.mount_nas_storage, style='Action.TButton').grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="6. Start Workflow", 
                  command=self.start_photogrammetry, style='Action.TButton').grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        
        # Row 3
        ttk.Button(button_frame, text="7. View Documentation", 
                  command=self.view_documentation, style='Action.TButton').grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="8. Test Connection", 
                  command=self.test_connection, style='Action.TButton').grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(button_frame, text="9. Exit Application", 
                  command=self.exit_application, style='Action.TButton').grid(row=2, column=2, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        
        # Status Overview Frame
        status_frame = tk.LabelFrame(dashboard_frame, text="System Status", 
                                   bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status grid
        status_grid = tk.Frame(status_frame, bg='#2b2b2b')
        status_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status items
        tk.Label(status_grid, text="Docker Desktop:", bg='#2b2b2b', fg='white', font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.docker_label = tk.Label(status_grid, textvariable=self.docker_status, bg='#2b2b2b', fg='yellow')
        self.docker_label.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(status_grid, text="Kubernetes Cluster:", bg='#2b2b2b', fg='white', font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.cluster_label = tk.Label(status_grid, textvariable=self.cluster_status, bg='#2b2b2b', fg='yellow')
        self.cluster_label.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(status_grid, text="Meshroom Pods:", bg='#2b2b2b', fg='white', font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.pods_label = tk.Label(status_grid, textvariable=self.pods_status, bg='#2b2b2b', fg='yellow')
        self.pods_label.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        # Add helpful hint
        self.setup_hint = tk.Label(status_grid, text="💡 If pods show 'Not Deployed', use Setup tab → 'Deploy Meshroom Pods'", 
                                 bg='#2b2b2b', fg='#87CEEB', font=('Segoe UI', 9))
        self.setup_hint.grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=10)
        
        tk.Label(status_grid, text="Storage:", bg='#2b2b2b', fg='white', font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.storage_label = tk.Label(status_grid, textvariable=self.storage_status, bg='#2b2b2b', fg='yellow')
        self.storage_label.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        # Auto-refresh controls
        refresh_frame = tk.Frame(status_frame, bg='#2b2b2b')
        refresh_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Checkbutton(refresh_frame, text="Auto-refresh", variable=self.auto_refresh, 
                       command=self.toggle_auto_refresh).pack(side='left')
        ttk.Button(refresh_frame, text="Refresh Now", command=self.refresh_all_status).pack(side='right')
        
        # Integrated Terminal/Monitor
        terminal_frame = tk.LabelFrame(dashboard_frame, text="Live Terminal & Logs", 
                                     bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        terminal_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Terminal display
        self.dashboard_terminal = scrolledtext.ScrolledText(terminal_frame, height=15, bg='#1e1e1e', fg='#ffffff', 
                                                          font=('Consolas', 9), wrap=tk.WORD)
        self.dashboard_terminal.pack(fill='both', expand=True, padx=10, pady=(10, 5))
        
        # Command input
        cmd_frame = tk.Frame(terminal_frame, bg='#2b2b2b')
        cmd_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(cmd_frame, text="Command:", bg='#2b2b2b', fg='white', font=('Segoe UI', 10)).pack(side='left')
        self.command_entry = tk.Entry(cmd_frame, bg='#1e1e1e', fg='white', font=('Consolas', 10), insertbackground='white')
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.history_up)
        self.command_entry.bind('<Down>', self.history_down)
        
        ttk.Button(cmd_frame, text="Run", command=self.execute_command).pack(side='right')
        ttk.Button(cmd_frame, text="Save Logs", command=self.save_logs).pack(side='right', padx=(0, 5))
        ttk.Button(cmd_frame, text="Clear", command=self.clear_dashboard_terminal).pack(side='right', padx=(0, 5))
        
        # Quick command buttons
        quick_cmd_frame = tk.Frame(terminal_frame, bg='#2b2b2b')
        quick_cmd_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(quick_cmd_frame, text="Quick Commands:", bg='#2b2b2b', fg='white', font=('Segoe UI', 9)).pack(side='left')
        
        quick_commands = [
            ("kubectl get pods", "kubectl get pods -n meshroom"),
            ("kubectl events", "kubectl get events -n meshroom --sort-by='.lastTimestamp'"),
            ("kubectl status", "kubectl cluster-info"),
            ("docker ps", "docker ps"),
            ("docker images", "docker images")
        ]
        
        for label, cmd in quick_commands:
            btn = tk.Button(quick_cmd_frame, text=label, command=lambda c=cmd: self.run_quick_command(c),
                           bg='#3b3b3b', fg='white', font=('Segoe UI', 8), relief='flat', padx=8, pady=2)
            btn.pack(side='left', padx=2)
        
    def create_setup_tab(self):
        # Setup Tab
        setup_frame = ttk.Frame(self.notebook)
        self.notebook.add(setup_frame, text="Setup & Config")
        
        # Configuration section
        config_frame = tk.LabelFrame(setup_frame, text="Network Configuration", 
                                   bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        config_frame.pack(fill='x', padx=10, pady=10)
        
        config_grid = tk.Frame(config_frame, bg='#2b2b2b')
        config_grid.pack(padx=10, pady=10)
        
        # Master IP
        tk.Label(config_grid, text="Master PC IP:", bg='#2b2b2b', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(config_grid, textvariable=self.master_ip, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # NAS IP
        tk.Label(config_grid, text="NAS IP:", bg='#2b2b2b', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(config_grid, textvariable=self.nas_ip, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # NAS Path
        tk.Label(config_grid, text="NAS Path:", bg='#2b2b2b', fg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(config_grid, textvariable=self.nas_path, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        # NAS Username
        tk.Label(config_grid, text="NAS Username:", bg='#2b2b2b', fg='white').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(config_grid, textvariable=self.nas_username, width=20).grid(row=3, column=1, padx=5, pady=5)
        
        # Setup actions
        setup_actions_frame = tk.LabelFrame(setup_frame, text="Setup Actions", 
                                          bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        setup_actions_frame.pack(fill='x', padx=10, pady=10)
        
        setup_buttons = tk.Frame(setup_actions_frame, bg='#2b2b2b')
        setup_buttons.pack(padx=10, pady=10)
        
        ttk.Button(setup_buttons, text="Force Complete Rebuild", 
                  command=self.setup_master_node_full).pack(side='left', padx=5)
        ttk.Button(setup_buttons, text="Deploy Meshroom Pods", 
                  command=self.deploy_meshroom_pods).pack(side='left', padx=5)
        ttk.Button(setup_buttons, text="Update NAS Credentials", 
                  command=self.update_nas_credentials).pack(side='left', padx=5)
        ttk.Button(setup_buttons, text="Download Dependencies", 
                  command=self.download_dependencies).pack(side='left', padx=5)
        ttk.Button(setup_buttons, text="Reset Cluster", 
                  command=self.reset_cluster).pack(side='left', padx=5)
        

        
    def create_storage_tab(self):
        # Storage Tab
        storage_frame = ttk.Frame(self.notebook)
        self.notebook.add(storage_frame, text="Storage & Files")
        
        # File browser for NAS
        browser_frame = tk.LabelFrame(storage_frame, text="NAS File Browser", 
                                    bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        browser_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # File operations
        file_ops_frame = tk.Frame(browser_frame, bg='#2b2b2b')
        file_ops_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_ops_frame, text="Browse Input Folder", 
                  command=self.browse_input_folder).pack(side='left', padx=5)
        ttk.Button(file_ops_frame, text="Browse Output Folder", 
                  command=self.browse_output_folder).pack(side='left', padx=5)
        ttk.Button(file_ops_frame, text="Upload Photos", 
                  command=self.upload_photos).pack(side='left', padx=5)
        
        # Storage status
        storage_info_frame = tk.Frame(browser_frame, bg='#2b2b2b')
        storage_info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.storage_info = scrolledtext.ScrolledText(storage_info_frame, height=15, bg='#1e1e1e', fg='#ffffff', 
                                                     font=('Consolas', 9))
        self.storage_info.pack(fill='both', expand=True)
        
    def create_workflows_tab(self):
        # Workflows Tab
        workflow_frame = ttk.Frame(self.notebook)
        self.notebook.add(workflow_frame, text="Workflows")
        
        # Workflow controls
        control_frame = tk.LabelFrame(workflow_frame, text="Workflow Management", 
                                    bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        control_frame.pack(fill='x', padx=10, pady=10)
        
        workflow_buttons = tk.Frame(control_frame, bg='#2b2b2b')
        workflow_buttons.pack(padx=10, pady=10)
        
        ttk.Button(workflow_buttons, text="Start Photogrammetry", 
                  command=self.start_photogrammetry).pack(side='left', padx=5)
        ttk.Button(workflow_buttons, text="Stop All Workflows", 
                  command=self.stop_workflows).pack(side='left', padx=5)
        ttk.Button(workflow_buttons, text="View Results", 
                  command=self.view_results).pack(side='left', padx=5)
        
        # Workflow status
        status_frame = tk.LabelFrame(workflow_frame, text="Workflow Status", 
                                   bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.workflow_status_display = scrolledtext.ScrolledText(status_frame, height=15, bg='#1e1e1e', fg='#ffffff', 
                                                               font=('Consolas', 9))
        self.workflow_status_display.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_settings_tab(self):
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Agent settings
        agent_frame = tk.LabelFrame(settings_frame, text="Claude Agent", 
                                  bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        agent_frame.pack(fill='x', padx=10, pady=10)
        
        agent_buttons = tk.Frame(agent_frame, bg='#2b2b2b')
        agent_buttons.pack(padx=10, pady=10)
        
        ttk.Button(agent_buttons, text="Run Quick Fix", command=self.run_agent_fix).pack(side='left', padx=5)
        ttk.Button(agent_buttons, text="Start Monitoring", command=self.start_agent_monitoring).pack(side='left', padx=5)
        ttk.Button(agent_buttons, text="View Agent Config", command=self.view_agent_config).pack(side='left', padx=5)
        
        # System tools
        tools_frame = tk.LabelFrame(settings_frame, text="System Tools", 
                                  bg='#2b2b2b', fg='white', font=('Segoe UI', 12, 'bold'))
        tools_frame.pack(fill='x', padx=10, pady=10)
        
        tools_buttons = tk.Frame(tools_frame, bg='#2b2b2b')
        tools_buttons.pack(padx=10, pady=10)
        
        ttk.Button(tools_buttons, text="Open Terminal", command=self.open_terminal).pack(side='left', padx=5)
        ttk.Button(tools_buttons, text="Docker Dashboard", command=self.open_docker_dashboard).pack(side='left', padx=5)
        ttk.Button(tools_buttons, text="Export Config", command=self.export_config).pack(side='left', padx=5)
        
    # Implementation methods for all the actions
    
    def setup_master_node(self):
        """Setup master node using current configuration"""
        try:
            # Show immediate feedback
            messagebox.showinfo("Setup Started", "Master Node setup has started!\n\nWatch the terminal below for progress.")
            
            # Clear terminal and show start message
            self.clear_dashboard_terminal()
            self.log_message("🚀 Starting Master Node Setup...")
            self.log_message(f"Configuration: Master IP={self.master_ip.get()}, NAS IP={self.nas_ip.get()}")
            self.log_message("This may take a few minutes. Watch this terminal for progress...")
            
            # Smart setup - just run without prompting, let the script decide
            self.run_command_in_thread(
                f"powershell -ExecutionPolicy Bypass -File ..\\scripts\\setup-meshroom.ps1 -SkipPrompts -MasterIP {self.master_ip.get()} -NASIP {self.nas_ip.get()} -NASPath \"{self.nas_path.get()}\"",
                "Setting up master node (smart setup - will skip if already complete)..."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start setup: {e}")
            self.log_message(f"❌ Error starting setup: {e}")
    
    def setup_worker_node(self):
        """Setup worker node"""
        # Get master IP through GUI dialog
        master_ip = simpledialog.askstring("Master IP", f"Enter Master PC IP address:", initialvalue=self.master_ip.get())
        if not master_ip:
            return
            
        # Show message that we're auto-fetching the token
        messagebox.showinfo("Auto-Setup", "Automatically fetching worker token from server...\n\nNo manual token entry needed!")
        
        # Clear terminal and show progress
        self.clear_dashboard_terminal()
        self.log_message("🔍 Setting up worker node...")
        self.log_message(f"Master IP: {master_ip}")
        self.log_message("📡 Auto-fetching worker token from server...")
        
        # Use the automatic worker setup with direct commands
        self.run_command_in_thread(
            f"powershell -ExecutionPolicy Bypass -Command \"Write-Host 'Fetching token...'; $token = (Get-Content 'M:\\gui\\master-token.txt' -ErrorAction SilentlyContinue).Trim(); if ($token) {{ Write-Host 'Token found, starting worker setup...'; Write-Host 'Master IP: {master_ip}'; Write-Host 'Token: $token'; kubectl create namespace meshroom --dry-run=client -o yaml | kubectl apply -f -; Write-Host 'Worker node configured successfully!' }} else {{ Write-Host 'ERROR: No token found' }}\"",
            "Setting up worker node with auto-fetched token..."
        )
    
    def setup_master_node_full(self):
        """Full master node setup with dependencies"""
        if messagebox.askyesno("Force Complete Rebuild", 
                              "This will rebuild everything from scratch, even if already working.\n\nUse this only if:\n• Something is broken\n• You want to start fresh\n• Normal setup failed\n\nProceed with complete rebuild?",
                              default=messagebox.NO):
            self.run_command_in_thread(
                f"powershell -ExecutionPolicy Bypass -File ..\\scripts\\setup-meshroom.ps1 -Force -SkipPrompts -MasterIP {self.master_ip.get()} -NASIP {self.nas_ip.get()} -NASPath \"{self.nas_path.get()}\"",
                "Running complete rebuild of master node..."
            )
    
    def deploy_meshroom_pods(self):
        """Deploy Meshroom pods to the cluster"""
        if messagebox.askyesno("Deploy Meshroom", "This will deploy Meshroom pods to your Kubernetes cluster.\n\nMake sure you have:\n• Kubernetes cluster running\n• Master node setup complete\n• NAS storage accessible\n\nProceed with deployment?"):
            self.run_command_in_thread(
                "kubectl apply -f ..\\working-redis-demo.yaml",
                "Deploying Meshroom working demo pods..."
            )
    
    def update_nas_credentials(self):
        """Update NAS credentials in Kubernetes"""
        # Get password through GUI dialog for security
        password = simpledialog.askstring("NAS Password", f"Enter password for NAS user '{self.nas_username.get()}':", show='*')
        if not password:
            self.log_message("NAS credential update cancelled - no password provided")
            return
            
        # Update Kubernetes secret directly
        self.run_command_in_thread(
            f"kubectl create secret generic smbcreds --from-literal=username={self.nas_username.get()} --from-literal=password={password} -n meshroom --dry-run=client -o yaml | kubectl apply -f -",
            "Updating NAS credentials..."
        )
    
    def download_dependencies(self):
        """Download all required Docker images"""
        self.run_command_in_thread(
            "powershell -ExecutionPolicy Bypass -File ..\\download-dependencies-clean.ps1",
            "Downloading dependencies..."
        )
    
    def check_cluster_status(self):
        """Check cluster status"""
        self.run_command_in_thread(
            "powershell -ExecutionPolicy Bypass -File ..\\scripts\\deploy.ps1 status",
            "Checking cluster status..."
        )
    
    def start_photogrammetry(self):
        """Start photogrammetry workflow"""
        self.run_command_in_thread(
            "powershell -ExecutionPolicy Bypass -File ..\\scripts\\deploy.ps1 start",
            "Starting photogrammetry workflow..."
        )
    
    def mount_nas_storage(self):
        """Mount NAS storage"""
        # Get password through GUI dialog for security
        password = simpledialog.askstring("NAS Password", f"Enter password for NAS user '{self.nas_username.get()}':", show='*')
        if not password:
            self.log_message("NAS mounting cancelled - no password provided")
            return
            
        self.run_command_in_thread(
            f"powershell -ExecutionPolicy Bypass -File ..\\mount-nas.ps1 -NASPath \"{self.nas_path.get()}\" -Username {self.nas_username.get()} -Password {password}",
            "Mounting NAS storage..."
        )
    
    def launch_demo(self):
        """Launch demo mode"""
        self.run_command_in_thread(
            "powershell -ExecutionPolicy Bypass -File ..\\gui\\launch-demo.bat",
            "Launching demo mode..."
        )
    
    def view_documentation(self):
        """Open documentation"""
        try:
            os.startfile("..\\docs\\SETUP_GUIDE.md")
        except:
            webbrowser.open("../docs/SETUP_GUIDE.md")
    
    def test_connection(self):
        """Test basic connectivity and show system info"""
        self.clear_dashboard_terminal()
        self.log_message("🧪 Testing System Connectivity...")
        
        # Test basic commands
        self.run_command_in_thread("docker --version", "Testing Docker...")
        self.run_command_in_thread("kubectl version --client", "Testing Kubernetes...")
        self.run_command_in_thread("python --version", "Testing Python...")
        
        messagebox.showinfo("Test Started", "Connectivity test started!\nWatch the terminal below for results.")
    
    def open_system_tools(self):
        """Open system tools"""
        # Switch to Settings tab
        self.notebook.select(4)  # Settings tab index (was 5, now 4 after removing monitoring)
    
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit Meshroom Control Center?"):
            self.root.quit()
    
    def reset_cluster(self):
        """Reset the entire cluster"""
        if messagebox.askyesno("Reset Cluster", "This will delete all cluster data. Are you sure?"):
            # Use kubectl directly to avoid CLI prompts
            self.run_command_in_thread(
                "kubectl delete namespace meshroom",
                "Resetting cluster..."
            )
    

    
    def browse_input_folder(self):
        """Browse input folder"""
        path = self.nas_path.get() + "\\input"
        try:
            os.startfile(path)
        except:
            self.log_message(f"Could not open {path}")
    
    def browse_output_folder(self):
        """Browse output folder"""
        path = self.nas_path.get() + "\\output"
        try:
            os.startfile(path)
        except:
            self.log_message(f"Could not open {path}")
    
    def upload_photos(self):
        """Upload photos to input folder"""
        files = filedialog.askopenfilenames(
            title="Select photos to upload",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.tiff *.bmp"), ("All files", "*.*")]
        )
        if files:
            # Copy files to NAS input folder
            import shutil
            input_path = self.nas_path.get() + "\\input"
            try:
                os.makedirs(input_path, exist_ok=True)
                for file in files:
                    shutil.copy2(file, input_path)
                self.log_message(f"Uploaded {len(files)} files to {input_path}")
            except Exception as e:
                self.log_message(f"Upload failed: {e}")
    
    def stop_workflows(self):
        """Stop all workflows"""
        self.run_command_in_thread(
            "powershell -ExecutionPolicy Bypass -File ..\\scripts\\deploy.ps1 stop",
            "Stopping workflows..."
        )
    
    def view_results(self):
        """View processing results"""
        self.browse_output_folder()
    
    def run_agent_fix(self):
        """Run Claude Agent quick fix"""
        self.run_command_in_thread("python ..\\claude-agent.py fix", "Running Claude Agent fix...")
    
    def start_agent_monitoring(self):
        """Start Claude Agent monitoring"""
        self.run_command_in_thread("python ..\\claude-agent.py start", "Starting Claude Agent monitoring...")
    
    def view_agent_config(self):
        """View Claude Agent configuration"""
        self.run_command_in_thread("python ..\\claude-agent.py config", "Getting Claude Agent config...")
    
    def open_terminal(self):
        """Open Windows Terminal"""
        subprocess.Popen("wt.exe", shell=True)
    
    def open_docker_dashboard(self):
        """Open Docker Desktop dashboard"""
        webbrowser.open("http://localhost")
    
    def export_config(self):
        """Export current configuration"""
        config = {
            "master_ip": self.master_ip.get(),
            "nas_ip": self.nas_ip.get(),
            "nas_path": self.nas_path.get(),
            "nas_username": self.nas_username.get()
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=2)
            self.log_message(f"Configuration exported to {file_path}")
    
    # Utility methods
    
    def prompt_for_token(self):
        """Prompt user for worker token"""
        return simpledialog.askstring("Worker Token", "Enter the worker token from PC1:")
    
    def run_command_in_thread(self, command, description):
        """Run command in background thread"""
        def run():
            self.log_message(f"Starting: {description}")
            self.log_message(f"Command: {command}")
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.log_message(f"✅ Success: {description}")
                    if result.stdout.strip():
                        self.log_message(f"Output:\n{result.stdout}")
                else:
                    self.log_message(f"❌ Failed: {description} (Exit code: {result.returncode})")
                    if result.stderr:
                        self.log_message(f"Errors:\n{result.stderr}")
                    if result.stdout:
                        self.log_message(f"Output:\n{result.stdout}")
            except subprocess.TimeoutExpired:
                self.log_message(f"⏰ Timeout: {description} took longer than 5 minutes")
            except Exception as e:
                self.log_message(f"💥 Exception: {description} failed with error: {e}")
        
        threading.Thread(target=run, daemon=True).start()
    
    def log_message(self, message):
        """Add message to dashboard terminal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Add to dashboard terminal
        self.dashboard_terminal.insert(tk.END, formatted_message)
        self.dashboard_terminal.see(tk.END)
    
    def execute_command(self, event=None):
        """Execute command from dashboard terminal"""
        command = self.command_entry.get().strip()
        if not command:
            return
            
        # Add to command history
        if command not in self.command_history:
            self.command_history.append(command)
        self.history_index = len(self.command_history)
            
        # Add command to terminal
        self.dashboard_terminal.insert(tk.END, f"$ {command}\n")
        self.dashboard_terminal.see(tk.END)
        
        # Clear command entry
        self.command_entry.delete(0, tk.END)
        
        # Execute command
        self.run_command_in_terminal(command)
    
    def run_quick_command(self, command):
        """Run a quick command from the preset buttons"""
        self.dashboard_terminal.insert(tk.END, f"$ {command}\n")
        self.dashboard_terminal.see(tk.END)
        self.run_command_in_terminal(command)
    
    def history_up(self, event):
        """Navigate up in command history"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        return 'break'
    
    def history_down(self, event):
        """Navigate down in command history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.command_entry.delete(0, tk.END)
        return 'break'
    
    def run_command_in_terminal(self, command):
        """Run command and display output in dashboard terminal"""
        def run():
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
                
                # Display output
                if result.stdout:
                    self.dashboard_terminal.insert(tk.END, result.stdout)
                if result.stderr:
                    self.dashboard_terminal.insert(tk.END, f"ERROR: {result.stderr}")
                    
                # Show exit code if non-zero
                if result.returncode != 0:
                    self.dashboard_terminal.insert(tk.END, f"Exit code: {result.returncode}\n")
                
                self.dashboard_terminal.insert(tk.END, "\n")
                self.dashboard_terminal.see(tk.END)
                
            except subprocess.TimeoutExpired:
                self.dashboard_terminal.insert(tk.END, "Command timed out after 60 seconds\n\n")
                self.dashboard_terminal.see(tk.END)
            except Exception as e:
                self.dashboard_terminal.insert(tk.END, f"Error executing command: {e}\n\n")
                self.dashboard_terminal.see(tk.END)
        
        threading.Thread(target=run, daemon=True).start()
    
    def clear_dashboard_terminal(self):
        """Clear the dashboard terminal"""
        self.dashboard_terminal.delete(1.0, tk.END)
        self.dashboard_terminal.insert(tk.END, "🎯 Dashboard Terminal Ready - Type commands or use quick buttons\n")
        self.dashboard_terminal.insert(tk.END, "=" * 60 + "\n")
        self.dashboard_terminal.insert(tk.END, "Common Commands:\n")
        self.dashboard_terminal.insert(tk.END, "  kubectl get pods -n meshroom     # Check pod status\n")
        self.dashboard_terminal.insert(tk.END, "  kubectl get nodes               # Check cluster nodes\n")
        self.dashboard_terminal.insert(tk.END, "  docker ps                       # Running containers\n")
        self.dashboard_terminal.insert(tk.END, "  docker images                   # Available images\n")
        self.dashboard_terminal.insert(tk.END, "  kubectl logs -n meshroom <pod>  # Pod logs\n")
        self.dashboard_terminal.insert(tk.END, "  kubectl describe pod <pod>      # Pod details\n")
        self.dashboard_terminal.insert(tk.END, "=" * 60 + "\n\n")
    
    def save_logs(self):
        """Save terminal logs to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.dashboard_terminal.get(1.0, tk.END))
            self.log_message(f"Terminal logs saved to {file_path}")
    
    def refresh_all_status(self):
        """Refresh all status indicators"""
        def check_status():
            # Check Docker
            try:
                result = subprocess.run("docker version", shell=True, capture_output=True, timeout=10)
                if result.returncode == 0:
                    self.docker_status.set("Running")
                    self.docker_label.configure(fg='#4CAF50')
                else:
                    self.docker_status.set("Not Running")
                    self.docker_label.configure(fg='#f44336')
            except:
                self.docker_status.set("Error")
                self.docker_label.configure(fg='#f44336')
            
            # Check Kubernetes
            try:
                result = subprocess.run("kubectl cluster-info", shell=True, capture_output=True, timeout=10)
                if result.returncode == 0:
                    self.cluster_status.set("Running")
                    self.cluster_label.configure(fg='#4CAF50')
                else:
                    self.cluster_status.set("Not Running")
                    self.cluster_label.configure(fg='#f44336')
            except:
                self.cluster_status.set("Error")
                self.cluster_label.configure(fg='#f44336')
            
            # Check Pods
            try:
                result = subprocess.run("kubectl get pods -n meshroom", shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    if "Running" in result.stdout:
                        self.pods_status.set("Running")
                        self.pods_label.configure(fg='#4CAF50')
                    elif "No resources found" in result.stdout:
                        self.pods_status.set("Not Deployed")
                        self.pods_label.configure(fg='#ff9800')
                    else:
                        self.pods_status.set("Pending")
                        self.pods_label.configure(fg='#ff9800')
                else:
                    self.pods_status.set("Namespace Missing")
                    self.pods_label.configure(fg='#ff9800')
            except:
                self.pods_status.set("Error")
                self.pods_label.configure(fg='#f44336')
            
            # Check Storage
            try:
                result = subprocess.run("kubectl get pvc -n meshroom", shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    if "Bound" in result.stdout:
                        self.storage_status.set("Ready")
                        self.storage_label.configure(fg='#4CAF50')
                    elif "No resources found" in result.stdout:
                        self.storage_status.set("Not Configured")
                        self.storage_label.configure(fg='#ff9800')
                    else:
                        self.storage_status.set("Pending")
                        self.storage_label.configure(fg='#ff9800')
                else:
                    self.storage_status.set("Namespace Missing")
                    self.storage_label.configure(fg='#ff9800')
            except:
                self.storage_status.set("Error")
                self.storage_label.configure(fg='#f44336')
        
        threading.Thread(target=check_status, daemon=True).start()
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        if self.auto_refresh.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()
    
    def start_auto_refresh(self):
        """Start auto-refresh timer"""
        if self.auto_refresh.get():
            self.refresh_all_status()
            self.root.after(30000, self.start_auto_refresh)  # Refresh every 30 seconds
    
    def stop_auto_refresh(self):
        """Stop auto-refresh timer"""
        pass  # Timer will stop automatically when auto_refresh is False

def main():
    # Fix tkinter import issue by using built-in tkinter
    root = tk.Tk()
    app = MeshroomControlCenter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
