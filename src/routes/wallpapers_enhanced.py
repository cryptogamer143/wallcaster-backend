from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
import os
import json
from src.models.user import db, User
from src.models.wallpaper import Wallpaper
from src.models.analytics import AnalyticsEvent
from src.utils.file_handler import save_uploaded_file, delete_file

wallpapers_enhanced_bp = Blueprint('wallpapers_enhanced', __name__)

# Upload folder configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')

@wallpapers_enhanced_bp.route('/api/wallpapers', methods=['GET'])
def get_wallpapers():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        status = request.args.get('status')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        query = Wallpaper.query
        
        # Apply filters
        if category:
            query = query.filter(Wallpaper.category == category)
        if status:
            query = query.filter(Wallpaper.status == status)
        if search:
            query = query.filter(
                Wallpaper.title.contains(search) | 
                Wallpaper.description.contains(search) |
                Wallpaper.tags.contains(search)
            )
        
        # Apply sorting
        if hasattr(Wallpaper, sort_by):
            if order == 'desc':
                query = query.order_by(getattr(Wallpaper, sort_by).desc())
            else:
                query = query.order_by(getattr(Wallpaper, sort_by))
        
        # Paginate
        wallpapers = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'wallpapers': [w.to_dict() for w in wallpapers.items],
            'total': wallpapers.total,
            'pages': wallpapers.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': wallpapers.has_next,
            'has_prev': wallpapers.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/<int:wallpaper_id>', methods=['GET'])
def get_wallpaper(wallpaper_id):
    try:
        wallpaper = Wallpaper.query.get_or_404(wallpaper_id)
        
        # Track view event
        event = AnalyticsEvent(
            event_type='view',
            wallpaper_id=wallpaper_id,
            user_id=session.get('user_id'),
            session_id=session.get('session_id'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(event)
        
        # Increment view count
        wallpaper.views += 1
        db.session.commit()
        
        return jsonify({'wallpaper': wallpaper.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers', methods=['POST'])
def create_wallpaper():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        title = request.form.get('title')
        description = request.form.get('description', '')
        category = request.form.get('category')
        tags = request.form.get('tags', '[]')
        
        if not title or not category:
            return jsonify({'error': 'Title and category are required'}), 400
        
        # Save uploaded file
        file_info, error = save_uploaded_file(file, UPLOAD_FOLDER)
        if error:
            return jsonify({'error': error}), 400
        
        # Create wallpaper record
        wallpaper = Wallpaper(
            title=title,
            description=description,
            filename=file_info['filename'],
            thumbnail_filename=file_info['thumbnail_filename'],
            category=category,
            tags=tags,
            resolution=file_info['resolution'],
            file_size=file_info['file_size'],
            uploaded_by=user_id
        )
        
        db.session.add(wallpaper)
        db.session.commit()
        
        return jsonify({
            'message': 'Wallpaper uploaded successfully',
            'wallpaper': wallpaper.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/<int:wallpaper_id>', methods=['PUT'])
def update_wallpaper(wallpaper_id):
    try:
        user_id = session.get('user_id')
        user_role = session.get('role')
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        wallpaper = Wallpaper.query.get_or_404(wallpaper_id)
        
        # Check permissions
        if wallpaper.uploaded_by != user_id and user_role not in ['admin', 'moderator']:
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'title' in data:
            wallpaper.title = data['title']
        if 'description' in data:
            wallpaper.description = data['description']
        if 'category' in data:
            wallpaper.category = data['category']
        if 'tags' in data:
            wallpaper.tags = data['tags']
        if 'status' in data and user_role in ['admin', 'moderator']:
            wallpaper.status = data['status']
        if 'featured' in data and user_role in ['admin', 'moderator']:
            wallpaper.featured = data['featured']
        if 'premium' in data and user_role in ['admin', 'moderator']:
            wallpaper.premium = data['premium']
        
        wallpaper.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Wallpaper updated successfully',
            'wallpaper': wallpaper.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/<int:wallpaper_id>', methods=['DELETE'])
def delete_wallpaper(wallpaper_id):
    try:
        user_id = session.get('user_id')
        user_role = session.get('role')
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        wallpaper = Wallpaper.query.get_or_404(wallpaper_id)
        
        # Check permissions
        if wallpaper.uploaded_by != user_id and user_role not in ['admin', 'moderator']:
            return jsonify({'error': 'Permission denied'}), 403
        
        # Delete files
        if wallpaper.filename:
            file_path = os.path.join(UPLOAD_FOLDER, wallpaper.filename)
            delete_file(file_path)
        
        if wallpaper.thumbnail_filename:
            thumbnail_path = os.path.join(UPLOAD_FOLDER, 'thumbnails', wallpaper.thumbnail_filename)
            delete_file(thumbnail_path)
        
        # Delete database record
        db.session.delete(wallpaper)
        db.session.commit()
        
        return jsonify({'message': 'Wallpaper deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/<int:wallpaper_id>/download', methods=['POST'])
def download_wallpaper(wallpaper_id):
    try:
        wallpaper = Wallpaper.query.get_or_404(wallpaper_id)
        
        # Track download event
        event = AnalyticsEvent(
            event_type='download',
            wallpaper_id=wallpaper_id,
            user_id=session.get('user_id'),
            session_id=session.get('session_id'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(event)
        
        # Increment download count
        wallpaper.downloads += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Download tracked',
            'download_url': f'/static/uploads/{wallpaper.filename}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/<int:wallpaper_id>/like', methods=['POST'])
def like_wallpaper(wallpaper_id):
    try:
        wallpaper = Wallpaper.query.get_or_404(wallpaper_id)
        
        # Track like event
        event = AnalyticsEvent(
            event_type='like',
            wallpaper_id=wallpaper_id,
            user_id=session.get('user_id'),
            session_id=session.get('session_id'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(event)
        
        # Increment like count
        wallpaper.likes += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Like recorded',
            'likes': wallpaper.likes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Wallpaper.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({'categories': category_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_enhanced_bp.route('/api/wallpapers/stats', methods=['GET'])
def get_wallpaper_stats():
    try:
        total_wallpapers = Wallpaper.query.count()
        pending_wallpapers = Wallpaper.query.filter_by(status='pending').count()
        approved_wallpapers = Wallpaper.query.filter_by(status='approved').count()
        featured_wallpapers = Wallpaper.query.filter_by(featured=True).count()
        
        # Recent uploads (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_uploads = Wallpaper.query.filter(Wallpaper.created_at >= week_ago).count()
        
        return jsonify({
            'total_wallpapers': total_wallpapers,
            'pending_wallpapers': pending_wallpapers,
            'approved_wallpapers': approved_wallpapers,
            'featured_wallpapers': featured_wallpapers,
            'recent_uploads': recent_uploads
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

