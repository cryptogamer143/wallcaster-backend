import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Generate a unique filename while preserving the extension"""
    ext = filename.rsplit('.', 1)[1].lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}"

def create_thumbnail(image_path, thumbnail_path, size=(300, 300)):
    """Create a thumbnail from an image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail maintaining aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save thumbnail
            img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return False

def get_image_info(image_path):
    """Get image dimensions and file size"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            file_size = os.path.getsize(image_path)
            return {
                'resolution': f"{width}x{height}",
                'file_size': file_size,
                'width': width,
                'height': height
            }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None

def save_uploaded_file(file, upload_folder):
    """Save uploaded file and create thumbnail"""
    try:
        if not file or file.filename == '':
            return None, "No file selected"
        
        if not allowed_file(file.filename):
            return None, "File type not allowed"
        
        # Create upload directory if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(os.path.join(upload_folder, 'thumbnails'), exist_ok=True)
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        # Save original file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Check file size
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            os.remove(file_path)
            return None, "File size too large (max 16MB)"
        
        # Get image info
        image_info = get_image_info(file_path)
        if not image_info:
            os.remove(file_path)
            return None, "Invalid image file"
        
        # Create thumbnail
        thumbnail_filename = f"thumb_{unique_filename.rsplit('.', 1)[0]}.jpg"
        thumbnail_path = os.path.join(upload_folder, 'thumbnails', thumbnail_filename)
        
        if not create_thumbnail(file_path, thumbnail_path):
            # If thumbnail creation fails, continue without it
            thumbnail_filename = None
        
        return {
            'filename': unique_filename,
            'thumbnail_filename': thumbnail_filename,
            'original_filename': original_filename,
            'file_path': file_path,
            'thumbnail_path': thumbnail_path if thumbnail_filename else None,
            **image_info
        }, None
        
    except Exception as e:
        return None, f"Error saving file: {str(e)}"

def delete_file(file_path):
    """Delete a file if it exists"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
    return False

