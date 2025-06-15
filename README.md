# Road Surveillance System - Lane Markings and Road Damage Detection

A comprehensive real-time surveillance system that uses machine learning to detect lane markings and road damage from video feeds and uploaded media files.

## Features

- **Real-time Detection**: Live camera feed processing for continuous monitoring
- **Batch Processing**: Upload and process video files and images
- **Machine Learning**: Advanced computer vision algorithms for accurate detection
- **Web Dashboard**: Modern React-based interface for monitoring and control
- **API Integration**: RESTful API for seamless frontend-backend communication
- **Statistics & Analytics**: Comprehensive reporting and data visualization

## System Architecture

\`\`\`
Frontend (Next.js)     Backend (Python)     ML Processing
     │                      │                    │
     ├─ Dashboard           ├─ Flask API         ├─ OpenCV
     ├─ File Upload         ├─ WebSocket         ├─ Lane Detection
     ├─ Live Feed           ├─ File Handler      ├─ Damage Detection
     └─ Statistics          └─ Database          └─ Image Processing
\`\`\`

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Webcam (for live detection)
- 4GB+ RAM recommended

## Installation & Setup

### Step 1: Clone and Setup Frontend

\`\`\`bash
# The Next.js frontend is already set up in this project
npm install
\`\`\`

### Step 2: Setup Python Environment

\`\`\`bash
# Create virtual environment (recommended)
python -m venv road_surveillance_env

# Activate virtual environment
# On Windows:
road_surveillance_env\Scripts\activate
# On macOS/Linux:
source road_surveillance_env/bin/activate

# Run the setup script
python scripts/setup_environment.py
\`\`\`

### Step 3: Install Additional Python Dependencies

\`\`\`bash
pip install opencv-python numpy pillow flask flask-cors websockets
\`\`\`

### Step 4: Create Required Directories

The setup script will create these automatically, but you can create them manually:

\`\`\`bash
mkdir uploads processed models logs temp
\`\`\`

## Running the System

### Method 1: Full System (Recommended)

1. **Start the Python API Server**:
\`\`\`bash
python scripts/api_server.py
\`\`\`
The API server will start on `http://localhost:5000`

2. **Start the Next.js Frontend**:
\`\`\`bash
npm run dev
\`\`\`
The web interface will be available at `http://localhost:3000`

### Method 2: Standalone ML Processing

\`\`\`bash
python scripts/ml_backend.py
\`\`\`

## Usage Guide

### 1. Live Detection
- Navigate to the "Live Detection" tab
- Click "Start Detection" to begin real-time processing
- The system will access your default camera
- Detections will appear in real-time on the dashboard

### 2. File Upload & Processing
- Go to the "Upload & Process" tab
- Select a video file (.mp4, .avi, .mov) or image (.jpg, .png)
- Click "Process File" to analyze the media
- Results will be displayed with confidence scores and locations

### 3. View Results
- Check the "Detection Results" tab for detailed analysis
- View detection statistics and severity levels
- Export results for further analysis

## API Endpoints

### Core Endpoints
- `GET /api/health` - System health check
- `POST /api/start_detection` - Start live detection
- `POST /api/stop_detection` - Stop live detection
- `GET /api/get_detections` - Get current detections
- `POST /api/upload_file` - Upload and process file
- `GET /api/get_statistics` - Get detection statistics

### Example API Usage

\`\`\`javascript
// Start detection
fetch('http://localhost:5000/api/start_detection', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ camera_id: 0 })
})

// Get detections
fetch('http://localhost:5000/api/get_detections')
  .then(response => response.json())
  .then(data => console.log(data.detections))
\`\`\`

## Configuration

Edit `config.json` to customize:

\`\`\`json
{
  "model_settings": {
    "lane_detection_threshold": 0.6,
    "damage_detection_threshold": 0.7,
    "min_contour_area": 100,
    "max_processing_fps": 30
  },
  "api_settings": {
    "host": "localhost",
    "port": 5000,
    "debug": true
  }
}
\`\`\`

## Detection Algorithms

### Lane Marking Detection
- **Preprocessing**: Gaussian blur and grayscale conversion
- **Edge Detection**: Canny edge detector
- **Line Detection**: Hough Line Transform
- **Filtering**: Angle and length-based filtering for lane-like features

### Road Damage Detection
- **Morphological Operations**: Top-hat and black-hat transforms
- **Contour Analysis**: Shape and size-based classification
- **Severity Assessment**: Area-based severity classification (low/medium/high)

## Troubleshooting

### Common Issues

1. **Camera not detected**:
   - Check camera permissions
   - Try different camera_id values (0, 1, 2...)
   - Ensure no other applications are using the camera

2. **Python dependencies error**:
   \`\`\`bash
   pip install --upgrade pip
   pip install opencv-python numpy pillow flask flask-cors
   \`\`\`

3. **Port already in use**:
   - Change port in `api_server.py` and update frontend API calls
   - Kill existing processes: `lsof -ti:5000 | xargs kill -9`

4. **File upload fails**:
   - Check file size (max 100MB by default)
   - Ensure uploads directory exists and has write permissions

### Performance Optimization

- Reduce processing FPS for better performance
- Use smaller input resolution for real-time processing
- Process every nth frame for video files
- Adjust detection thresholds based on your use case

## File Structure

\`\`\`
road-surveillance-system/
├── app/
│   ├── page.tsx              # Main dashboard
│   └── api/
│       ├── upload/route.ts   # File upload handler
│       └── process/route.ts  # Processing API
├── scripts/
│   ├── ml_backend.py         # ML processing core
│   ├── api_server.py         # Flask API server
│   └── setup_environment.py # Setup script
├── uploads/                  # Uploaded files
├── processed/               # Processing results
├── config.json             # Configuration
└── README.md               # This file
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue on the repository
