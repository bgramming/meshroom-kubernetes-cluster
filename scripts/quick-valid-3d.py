#!/usr/bin/env python3
"""
Quick Valid 3D File Generator
Creates small but properly formatted 3D files that Blender can actually open
No fake delays - instant results
"""

import os
import math
from datetime import datetime

# Configuration
NAS_INPUT = r"\\BernHQ\Big Pool\Shared Folders\Meshroom\input"
NAS_OUTPUT_BASE = r"\\BernHQ\Big Pool\Shared Folders\Meshroom\output"

def create_session_folder():
    """Create session folder"""
    os.makedirs(NAS_OUTPUT_BASE, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = f"quick_session_{timestamp}"
    session_path = os.path.join(NAS_OUTPUT_BASE, session_name)
    os.makedirs(session_path, exist_ok=True)
    return session_path, session_name

def create_simple_valid_ply(session_path, name="simple_pointcloud"):
    """Create a simple but VALID PLY file that Blender won't crash on"""
    ply_file = os.path.join(session_path, f"{name}.ply")
    
    # Create a simple cube point cloud (8 vertices)
    points = [
        [-1, -1, -1, 255, 0, 0],    # Red corner
        [ 1, -1, -1, 0, 255, 0],    # Green corner  
        [ 1,  1, -1, 0, 0, 255],    # Blue corner
        [-1,  1, -1, 255, 255, 0],  # Yellow corner
        [-1, -1,  1, 255, 0, 255],  # Magenta corner
        [ 1, -1,  1, 0, 255, 255],  # Cyan corner
        [ 1,  1,  1, 255, 255, 255], # White corner
        [-1,  1,  1, 128, 128, 128]  # Gray corner
    ]
    
    ply_content = f"""ply
format ascii 1.0
comment Simple test point cloud
element vertex {len(points)}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
    
    for point in points:
        x, y, z, r, g, b = point
        ply_content += f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\\n"
    
    with open(ply_file, 'w') as f:
        f.write(ply_content)
    
    return ply_file

def create_simple_valid_obj(session_path, name="simple_mesh"):
    """Create a simple but VALID OBJ file that Blender can open"""
    obj_file = os.path.join(session_path, f"{name}.obj")
    
    # Create a simple pyramid (4 vertices, 4 triangular faces)
    obj_content = """# Simple pyramid mesh
# Valid OBJ format for Blender

# Vertices
v 0.0 1.0 0.0
v -1.0 -1.0 1.0
v 1.0 -1.0 1.0
v 0.0 -1.0 -1.0

# Faces (triangles)
f 1 2 3
f 1 3 4
f 1 4 2
f 2 4 3
"""
    
    with open(obj_file, 'w') as f:
        f.write(obj_content)
    
    return obj_file

def create_better_valid_obj(session_path, name="detailed_mesh"):
    """Create a more detailed but still valid OBJ file"""
    obj_file = os.path.join(session_path, f"{name}.obj")
    
    obj_content = """# Detailed sphere mesh
# Valid OBJ format with more geometry

"""
    
    # Create a simple sphere with vertices
    vertices = []
    faces = []
    
    # Generate sphere vertices
    for i in range(10):  # 10 latitude lines
        lat = (i / 9.0) * math.pi - math.pi/2
        for j in range(20):  # 20 longitude lines
            lon = (j / 19.0) * 2 * math.pi
            
            x = math.cos(lat) * math.cos(lon)
            y = math.sin(lat)
            z = math.cos(lat) * math.sin(lon)
            
            vertices.append((x, y, z))
            obj_content += f"v {x:.6f} {y:.6f} {z:.6f}\\n"
    
    # Generate faces (triangles)
    for i in range(9):  # 9 latitude segments
        for j in range(19):  # 19 longitude segments
            # Calculate vertex indices (OBJ uses 1-based indexing)
            v1 = i * 20 + j + 1
            v2 = i * 20 + (j + 1) + 1
            v3 = (i + 1) * 20 + j + 1
            v4 = (i + 1) * 20 + (j + 1) + 1
            
            # Two triangles per quad
            obj_content += f"f {v1} {v2} {v3}\\n"
            obj_content += f"f {v2} {v4} {v3}\\n"
    
    with open(obj_file, 'w') as f:
        f.write(obj_content)
    
    return obj_file

def create_valid_stl(session_path, name="printable_model"):
    """Create a valid STL file for 3D printing"""
    stl_file = os.path.join(session_path, f"{name}.stl")
    
    stl_content = """solid SimpleModel
facet normal 0.0 0.0 1.0
  outer loop
    vertex 0.0 0.0 0.0
    vertex 1.0 0.0 0.0
    vertex 0.5 1.0 0.0
  endloop
endfacet
facet normal 0.0 0.0 -1.0
  outer loop
    vertex 0.0 0.0 -0.1
    vertex 0.5 1.0 -0.1
    vertex 1.0 0.0 -0.1
  endloop
endfacet
facet normal 0.0 -1.0 0.0
  outer loop
    vertex 0.0 0.0 0.0
    vertex 0.0 0.0 -0.1
    vertex 1.0 0.0 0.0
  endloop
endfacet
facet normal 0.0 -1.0 0.0
  outer loop
    vertex 1.0 0.0 0.0
    vertex 0.0 0.0 -0.1
    vertex 1.0 0.0 -0.1
  endloop
endfacet
endsolid SimpleModel
"""
    
    with open(stl_file, 'w') as f:
        f.write(stl_content)
    
    return stl_file

def install_real_meshroom_prompt():
    """Prompt user to install real Meshroom"""
    print()
    print("🎯 WANT REAL 3D RECONSTRUCTION?")
    print("=" * 35)
    print("For ACTUAL GPU processing that uses your Radeon RX 580:")
    print()
    print("1. Run: powershell -ExecutionPolicy Bypass .\\install-real-meshroom.ps1")
    print("2. This will download and install real Meshroom")
    print("3. Real Meshroom will:")
    print("   • Actually use your AMD GPU")
    print("   • Take 30+ minutes (real processing time)")
    print("   • Create high-quality 3D models")
    print("   • Make your GPU fans spin up")
    print()
    print("Or download manually from:")
    print("https://github.com/alicevision/Meshroom/releases")

def main():
    print("Quick Valid 3D File Generator")
    print("=" * 35)
    print("⚡ Creates small but valid 3D files instantly")
    print("🎯 Files that actually work in Blender")
    print("❌ No fake 58-minute delays")
    print()
    
    # Create session
    session_path, session_name = create_session_folder()
    print(f"Session: {session_name}")
    print(f"Output: {session_path}")
    print()
    
    print("Creating valid 3D files...")
    
    # Create files
    ply_file = create_simple_valid_ply(session_path)
    simple_obj = create_simple_valid_obj(session_path)
    detailed_obj = create_better_valid_obj(session_path)
    stl_file = create_valid_stl(session_path)
    
    # Create summary
    summary_file = os.path.join(session_path, "file_info.txt")
    with open(summary_file, 'w') as f:
        f.write(f"Quick 3D File Generation Results\\n")
        f.write(f"================================\\n")
        f.write(f"Session: {session_name}\\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Processing time: Instant (no fake delays)\\n")
        f.write(f"\\nGenerated Files:\\n")
        f.write(f"• {os.path.basename(ply_file)} - Simple point cloud (8 points)\\n")
        f.write(f"• {os.path.basename(simple_obj)} - Simple pyramid mesh\\n")
        f.write(f"• {os.path.basename(detailed_obj)} - Detailed sphere mesh\\n")
        f.write(f"• {os.path.basename(stl_file)} - 3D printable model\\n")
        f.write(f"\\nThese files should open properly in Blender!\\n")
    
    print("✅ Files created:")
    for file_path in [ply_file, simple_obj, detailed_obj, stl_file, summary_file]:
        size_kb = os.path.getsize(file_path) / 1024
        print(f"   • {os.path.basename(file_path)} ({size_kb:.1f} KB)")
    
    print()
    print("🎉 COMPLETE! Files ready for Blender")
    print(f"📁 Location: {session_path}")
    print()
    print("✅ These files should:")
    print("   • Open in Blender without crashing")
    print("   • Show actual 3D geometry")
    print("   • Import properly")
    
    install_real_meshroom_prompt()

if __name__ == "__main__":
    main()
