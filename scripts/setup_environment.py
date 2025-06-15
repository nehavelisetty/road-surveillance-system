import os
import subprocess
import sys

def install_requirements():
    """Install required Python packages"""
    requirements = [
        'opencv-python',
        'numpy',
        'pillow',
        'flask',
        'flask-cors',
        'websockets',
        'asyncio',
        'json',
        'datetime'
    ]
    
    print("Installing Python requirements...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'processed',
        'models',
        'logs',
        'temp'
    ]
    
    print("Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def setup_config():
    """Create configuration file"""
    config = {
        "model_settings": {
            "lane_detection_threshold": 0.6,
            "damage_detection_threshold": 0.7,
            "min_contour_area": 100,
            "max_processing_fps": 30
        },
        "api_settings": {
            "host": "localhost",
            "port": 5000,
            "debug": True
        },
        "file_settings": {
            "max_file_size_mb": 100,
            "allowed_extensions": [".mp4", ".avi", ".mov", ".jpg", ".jpeg", ".png"],
            "upload_path": "./uploads",
            "processed_path": "./processed"
        }
    }
    
    import json
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✓ Created configuration file")

def main():
    print("Setting up Road Surveillance System...")
    print("=" * 50)
    
    install_requirements()
    create_directories()
    setup_config()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the Next.js frontend: npm run dev")
    print("2. Run the Python backend: python ml_backend.py")
    print("3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()
