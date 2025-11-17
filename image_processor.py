"""
Image preprocessing module for defect detection system
"""
import cv2
import numpy as np
from scipy import ndimage


class ImageProcessor:
    """Handles image preprocessing operations"""
    
    def __init__(self):
        self.target_size = (640, 640)  # Standard size for YOLO models
    
    def preprocess(self, image_path):
        """
        Preprocess image: resize, noise removal, brightness adjustment
        
        Args:
            image_path: Path to input image
            
        Returns:
            Preprocessed image (numpy array)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to RGB (OpenCV reads as BGR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image
        image = self.resize(image)
        
        # Remove noise
        image = self.remove_noise(image)
        
        # Adjust brightness
        image = self.adjust_brightness(image)
        
        return image
    
    def resize(self, image, target_size=None):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image: Input image
            target_size: Target size (width, height). If None, uses default
            
        Returns:
            Resized image
        """
        if target_size is None:
            target_size = self.target_size
        
        height, width = image.shape[:2]
        target_width, target_height = target_size
        
        # Calculate scaling factor
        scale = min(target_width / width, target_height / height)
        
        # Resize
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Pad if necessary to match target size
        if new_width != target_width or new_height != target_height:
            pad_top = (target_height - new_height) // 2
            pad_bottom = target_height - new_height - pad_top
            pad_left = (target_width - new_width) // 2
            pad_right = target_width - new_width - pad_left
            
            resized = cv2.copyMakeBorder(
                resized, pad_top, pad_bottom, pad_left, pad_right,
                cv2.BORDER_CONSTANT, value=[0, 0, 0]
            )
        
        return resized
    
    def remove_noise(self, image, method='gaussian'):
        """
        Remove noise from image
        
        Args:
            image: Input image
            method: Noise removal method ('gaussian', 'median', 'bilateral')
            
        Returns:
            Denoised image
        """
        if method == 'gaussian':
            # Gaussian blur for noise reduction
            return cv2.GaussianBlur(image, (5, 5), 0)
        elif method == 'median':
            # Median filter (good for salt-and-pepper noise)
            return cv2.medianBlur(image, 5)
        elif method == 'bilateral':
            # Bilateral filter (preserves edges while reducing noise)
            return cv2.bilateralFilter(image, 9, 75, 75)
        else:
            return image
    
    def adjust_brightness(self, image, alpha=1.0, beta=0):
        """
        Adjust image brightness and contrast
        
        Args:
            image: Input image
            alpha: Contrast control (1.0 = no change)
            beta: Brightness control (0 = no change)
            
        Returns:
            Adjusted image
        """
        # Convert to float to avoid overflow
        image_float = image.astype(np.float32)
        
        # Apply brightness and contrast adjustment
        adjusted = alpha * image_float + beta
        
        # Clip values to valid range [0, 255]
        adjusted = np.clip(adjusted, 0, 255)
        
        return adjusted.astype(np.uint8)
    
    def enhance_contrast(self, image):
        """
        Enhance image contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        
        Args:
            image: Input image
            
        Returns:
            Contrast-enhanced image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels and convert back to RGB
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
        
        return enhanced
    
    def grayscale(self, image):
        """
        Convert image to grayscale
        
        Args:
            image: Input RGB image
            
        Returns:
            Grayscale image
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image
    
    def save_image(self, image, output_path):
        """
        Save image to file
        
        Args:
            image: Image to save (RGB format)
            output_path: Output file path
        """
        # Convert RGB to BGR for OpenCV
        if len(image.shape) == 3:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            image_bgr = image
        
        cv2.imwrite(output_path, image_bgr)

