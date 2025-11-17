# Quick Start Guide

## Installation Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create necessary directories (if not already created):**
   ```bash
   mkdir -p uploads static/processed reports models
   ```

3. **(Optional) Download YOLOv4-Tiny model files:**
   ```bash
   ./download_models.sh
   ```
   Or manually download:
   - `yolov4-tiny.cfg`
   - `yolov4-tiny.weights`
   - `coco.names`
   
   Place them in the `models/` directory.

## Running the Application

### Method 1: Direct Python
```bash
python app.py
```

### Method 2: Using the run script
```bash
./run.sh
```

The application will start on `http://localhost:5001`

## Login Credentials

- **Username:** `admin` | **Password:** `admin123`
- **Username:** `user` | **Password:** `user123`

## Usage Workflow

1. **Login** with your credentials
2. **Upload an image** from the dashboard or upload page
3. **View results** - The system will automatically:
   - Preprocess the image (resize, denoise, adjust brightness)
   - Detect defects using classical methods (and YOLO if available)
   - Display annotated image with bounding boxes
   - Show detailed detection information
4. **Generate PDF report** - Click the "Generate PDF Report" button to download a comprehensive report

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP

Maximum file size: 16MB

## Troubleshooting

### Issue: "YOLOv4-Tiny model files not found"
**Solution:** This is normal if you haven't downloaded the model files. The system will work using only classical image processing methods.

### Issue: "Module not found"
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Permission denied" when running scripts
**Solution:** Make scripts executable:
```bash
chmod +x run.sh download_models.sh
```

## Testing the System

1. Upload an image of a surface with visible cracks or irregularities
2. The system should detect and highlight defects
3. Check the results page for detailed information
4. Generate a PDF report to verify report generation

## Notes

- Processed images are stored in `static/processed/`
- Original uploads are stored in `uploads/`
- Generated reports are stored in `reports/`
- All data is stored locally on your machine

