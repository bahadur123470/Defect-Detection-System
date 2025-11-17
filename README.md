# Defect Detection System

An automated defect detection system for industrial pipelines and building surfaces using image processing techniques and YOLOv4-Tiny.

## Features

- **User Authentication**: Secure login/logout system
- **Image Upload**: Easy-to-use interface for uploading images
- **Image Preprocessing**: Automatic resizing, noise removal, and brightness adjustment
- **Defect Detection**: 
  - YOLOv4-Tiny integration for object detection
  - Classical image processing methods (edge detection, contour analysis) for crack and surface irregularity detection
- **Visualization**: Display processed images with bounding boxes highlighting detected defects
- **Report Generation**: Generate PDF reports with defect count, types, and annotated images

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. (Optional) Download YOLOv4-Tiny model files:
   - Download `yolov4-tiny.cfg` and `yolov4-tiny.weights` from [YOLO official repository](https://github.com/AlexeyAB/darknet)
   - Download `coco.names` from [COCO dataset](https://github.com/pjreddie/darknet/blob/master/data/coco.names)
   - Place these files in the `models/` directory

   **Note**: The system will work without YOLO model files using only classical image processing methods.

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Login with demo credentials:
   - Username: `admin` | Password: `admin123`
   - Username: `user` | Password: `user123`

4. Upload an image through the web interface

5. View detection results and generate PDF reports

## Project Structure

```
detectives/
├── app.py                 # Main Flask application
├── image_processor.py     # Image preprocessing module
├── defect_detector.py     # Defect detection module
├── report_generator.py    # PDF report generation
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   └── results.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── processed/       # Processed images storage
├── uploads/             # Uploaded images storage
├── models/              # YOLO model files (optional)
└── reports/             # Generated PDF reports
```

## Functional Requirements

✅ **FR1**: User authentication system with login/logout functionality  
✅ **FR2**: Image input system for capturing product images  
✅ **FR3**: Image preprocessing (resizing, noise removal, brightness adjustment)  
✅ **FR4**: Integration of pretrained object detection model (YOLOv4-Tiny)  
✅ **FR5**: Display of processed images with defects visually highlighted  
✅ **FR6**: Display of detected defects with highlighted areas  
✅ **FR7**: Report generation with defect count, defect type, and marked images  

## Technologies Used

- **Python**: Programming language
- **Flask**: Web framework
- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical operations
- **SciPy**: Scientific computing
- **ReportLab**: PDF generation
- **YOLOv4-Tiny**: Object detection model (optional)

## Detection Methods

### Classical Image Processing
- **Crack Detection**: Uses Canny edge detection and morphological operations to identify linear defects
- **Surface Irregularity Detection**: Uses adaptive thresholding and contour analysis

### Deep Learning (Optional)
- **YOLOv4-Tiny**: Pre-trained model for general object detection (requires model files)

## Notes

- The system works with or without YOLO model files
- Without YOLO, only classical image processing methods are used
- Image uploads are limited to 16MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP
- All processed images and reports are stored locally

## Security Considerations

⚠️ **Important**: This is a demo application. For production use:
- Change the secret key in `app.py`
- Use a proper database instead of in-memory user storage
- Implement proper session management
- Add input validation and sanitization
- Use HTTPS for secure communication
- Implement proper file upload security measures

## License

This project is for educational purposes.

## Author

Defect Detection System - Image Processing Project

