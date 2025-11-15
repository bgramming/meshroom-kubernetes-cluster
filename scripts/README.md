# Meshroom Processing Tools

Collection of standalone Meshroom processing scripts for 3D photogrammetry.

## Available Scripts

### Production Scripts

#### `realistic-meshroom-processing.py`
- **Purpose:** Actual 3D reconstruction with proper timing
- **Features:** Real 3D model creation, NAS integration
- **Status:** Production ready
- **Usage:** `python realistic-meshroom-processing.py`

#### `actual-meshroom-processing.py`
- **Purpose:** Production processing script
- **Features:** Complete photogrammetry pipeline
- **Status:** Production ready

#### `real-meshroom-processing.py`
- **Purpose:** Real Meshroom integration
- **Features:** Native Meshroom workflow
- **Status:** Production ready

### Simplified Scripts

#### `process-photos-simple.py`
- **Purpose:** Simplified photo processing workflow
- **Features:** Easy-to-use interface, basic processing
- **Status:** Ready for use
- **Best for:** Quick processing jobs

#### `process-photos.py`
- **Purpose:** Standard photo processing
- **Features:** Full feature set
- **Status:** Production ready

### Utility Scripts

#### `meshroom-native-processing.py`
- **Purpose:** Native Meshroom integration
- **Features:** Direct Meshroom API usage
- **Status:** Ready

#### `quick-valid-3d.py`
- **Purpose:** Fast 3D model validation
- **Features:** Quick checks, validation reports
- **Status:** Ready
- **Usage:** `python quick-valid-3d.py <model_path>`

## Requirements

Install dependencies:
```bash
pip install -r ../requirements.txt
```

## Configuration

Most scripts connect to NAS at:
- **Input:** `\\BernHQ\Big Pool\Shared Folders\Meshroom\input`
- **Output:** `\\BernHQ\Big Pool\Shared Folders\Meshroom\output`

Edit the scripts to change these paths if needed.

## Usage Examples

### Basic Processing
```bash
python realistic-meshroom-processing.py
```

### Quick Validation
```bash
python quick-valid-3d.py path/to/model.obj
```

### Simplified Workflow
```bash
python process-photos-simple.py
```

## Integration with Meshroom Cluster

These scripts can work alongside the Meshroom Kubernetes cluster:
- Use for single-PC processing
- Test workflows before cluster deployment
- Quick validation of results

## Troubleshooting

### NAS Connection Issues
- Verify network drive is mapped
- Check NAS IP address in scripts
- Ensure proper permissions

### Meshroom Not Found
- Install Meshroom: `03-Scripts\install-real-meshroom.ps1`
- Check Meshroom is in PATH
- Verify installation directory

### Python Errors
- Install requirements: `pip install -r ../requirements.txt`
- Check Python version (3.7+ required)
- Verify all dependencies installed

## Related

- **Meshroom Cluster:** `C:\Users\bgram\Programming\meshroom-app\`
- **Testing Tools:** `C:\Users\bgram\Programming\03-Scripts\Testing\`
- **Documentation:** `C:\Users\bgram\Programming\docs\`

