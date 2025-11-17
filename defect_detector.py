"""
Defect detection module using YOLOv4-Tiny and classical image processing
"""
import cv2
import numpy as np
from image_processor import ImageProcessor


class DefectDetector:
    """Detects defects in images using YOLOv4-Tiny and classical methods"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.yolo_model = None
        self.yolo_net = None
        self.yolo_classes = []
        self.use_yolo = False
        self._load_yolo_model()
    
    def _load_yolo_model(self):
        """Load YOLOv4-Tiny model if available"""
        try:
            # YOLOv4-Tiny configuration files
            config_path = 'models/yolov4-tiny.cfg'
            weights_path = 'models/yolov4-tiny.weights'
            classes_path = 'models/coco.names'
            
            # Check if model files exist
            import os
            if os.path.exists(config_path) and os.path.exists(weights_path):
                self.yolo_net = cv2.dnn.readNet(weights_path, config_path)
                self.yolo_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.yolo_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                
                # Load class names
                if os.path.exists(classes_path):
                    with open(classes_path, 'r') as f:
                        self.yolo_classes = [line.strip() for line in f.readlines()]
                
                self.use_yolo = True
                print("YOLOv4-Tiny model loaded successfully")
            else:
                print("YOLOv4-Tiny model files not found. Using classical methods only.")
                self.use_yolo = False
        except Exception as e:
            print(f"Error loading YOLO model: {e}. Using classical methods only.")
            self.use_yolo = False
    
    def detect(self, image):
        """
        Detect defects in image
        
        Args:
            image: Preprocessed image (RGB format)
            
        Returns:
            List of detection dictionaries with 'type', 'confidence', 'bbox'
        """
        detections = []
        
        if self.use_yolo:
            # Use YOLOv4-Tiny for detection
            yolo_detections = self._detect_with_yolo(image)
            detections.extend(yolo_detections)
        
        # Use classical methods for additional detection
        classical_detections = self._detect_with_classical(image)
        detections.extend(classical_detections)
        
        return detections
    
    def _detect_with_yolo(self, image):
        """Detect defects using YOLOv4-Tiny"""
        detections = []
        
        if self.yolo_net is None:
            return detections
        
        try:
            # Convert RGB to BGR for OpenCV
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            height, width = image_bgr.shape[:2]
            
            # Create blob from image
            blob = cv2.dnn.blobFromImage(
                image_bgr, 1/255.0, (416, 416), swapRB=True, crop=False
            )
            
            # Set input to network
            self.yolo_net.setInput(blob)
            
            # Get output layer names
            layer_names = self.yolo_net.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.yolo_net.getUnconnectedOutLayers()]
            
            # Forward pass
            outputs = self.yolo_net.forward(output_layers)
            
            # Process detections
            conf_threshold = 0.5
            nms_threshold = 0.4
            
            boxes = []
            confidences = []
            class_ids = []
            
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > conf_threshold:
                        # Get bounding box coordinates
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            
            # Apply Non-Maximum Suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
            
            if len(indices) > 0:
                for i in indices.flatten():
                    x, y, w, h = boxes[i]
                    class_name = self.yolo_classes[class_ids[i]] if class_ids[i] < len(self.yolo_classes) else "Unknown"
                    
                    detections.append({
                        'type': class_name,
                        'confidence': float(confidences[i]),
                        'bbox': [x, y, x + w, y + h]
                    })
        
        except Exception as e:
            print(f"Error in YOLO detection: {e}")
        
        return detections
    
    def _detect_with_classical(self, image):
        """Detect defects using classical image processing methods"""
        detections = []
        
        # Convert to grayscale
        gray = self.image_processor.grayscale(image)
        
        # Detect cracks using edge detection
        crack_detections = self._detect_cracks(gray)
        detections.extend(crack_detections)
        
        # Detect surface irregularities
        irregularity_detections = self._detect_surface_irregularities(gray)
        detections.extend(irregularity_detections)
        
        return detections
    
    def _detect_cracks(self, gray_image):
        """Detect cracks using edge detection and morphological operations"""
        detections = []
        
        try:
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
            
            # Canny edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Morphological operations to connect crack lines
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=2)
            closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=3)
            
            # Find contours
            contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area and aspect ratio (cracks are typically long and thin)
            min_area = 100
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = max(w, h) / max(min(w, h), 1)
                    
                    # Cracks typically have high aspect ratio
                    if aspect_ratio > 3:
                        detections.append({
                            'type': 'Crack',
                            'confidence': min(0.9, area / 1000),
                            'bbox': [x, y, x + w, y + h]
                        })
        
        except Exception as e:
            print(f"Error in crack detection: {e}")
        
        return detections
    
    def _detect_surface_irregularities(self, gray_image):
        """Detect surface irregularities using texture analysis"""
        detections = []
        
        try:
            # Apply adaptive thresholding
            adaptive_thresh = cv2.adaptiveThreshold(
                gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # Find contours
            contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter by area
            min_area = 200
            max_area = 50000
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if min_area < area < max_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate irregularity score based on contour complexity
                    perimeter = cv2.arcLength(contour, True)
                    circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
                    
                    # Low circularity indicates irregularity
                    if circularity < 0.5:
                        detections.append({
                            'type': 'Surface Irregularity',
                            'confidence': min(0.8, area / 5000),
                            'bbox': [x, y, x + w, y + h]
                        })
        
        except Exception as e:
            print(f"Error in surface irregularity detection: {e}")
        
        return detections
    
    def draw_detections(self, image, detections):
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Input image (RGB format)
            detections: List of detection dictionaries
            
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        # Color map for different defect types
        color_map = {
            'Crack': (255, 0, 0),  # Red
            'Surface Irregularity': (0, 255, 0),  # Green
            'Dent': (0, 0, 255),  # Blue
            'Leak': (255, 255, 0),  # Cyan
        }
        
        for det in detections:
            bbox = det['bbox']
            defect_type = det['type']
            confidence = det.get('confidence', 0.0)
            
            # Get color for defect type
            color = color_map.get(defect_type, (255, 255, 255))
            
            # Draw bounding box
            x1, y1, x2, y2 = bbox
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{defect_type}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            label_y = max(y1, label_size[1] + 10)
            
            # Draw label background
            cv2.rectangle(annotated, (x1, label_y - label_size[1] - 10),
                         (x1 + label_size[0], label_y), color, -1)
            
            # Draw label text
            cv2.putText(annotated, label, (x1, label_y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return annotated

