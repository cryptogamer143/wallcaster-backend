from flask import Blueprint, jsonify, request
import os
from datetime import datetime, timedelta
import random

wallpapers_bp = Blueprint('wallpapers', __name__)

# Sample wallpaper data
sample_wallpapers = [
    {
        'id': 1,
        'title': 'Mountain Landscape',
        'tags': ['nature', 'mountain', 'landscape'],
        'status': 'approved',
        'downloads': 1234,
        'upload_date': '2024-01-15',
        'uploader': 'user123',
        'file_size': '2.4 MB',
        'resolution': '1920x1080',
        'category': 'Nature'
    },
    {
        'id': 2,
        'title': 'City Skyline',
        'tags': ['city', 'urban', 'skyline'],
        'status': 'pending',
        'downloads': 567,
        'upload_date': '2024-01-20',
        'uploader': 'user456',
        'file_size': '3.1 MB',
        'resolution': '2560x1440',
        'category': 'Urban'
    },
    {
        'id': 3,
        'title': 'Ocean Waves',
        'tags': ['ocean', 'blue', 'waves'],
        'status': 'approved',
        'downloads': 890,
        'upload_date': '2024-01-18',
        'uploader': 'user789',
        'file_size': '1.8 MB',
        'resolution': '1920x1080',
        'category': 'Nature'
    },
    {
        'id': 4,
        'title': 'Forest Path',
        'tags': ['forest', 'green', 'path'],
        'status': 'flagged',
        'downloads': 234,
        'upload_date': '2024-01-22',
        'uploader': 'user101',
        'file_size': '2.7 MB',
        'resolution': '1920x1080',
        'category': 'Nature'
    },
    {
        'id': 5,
        'title': 'Desert Sunset',
        'tags': ['desert', 'sunset', 'orange'],
        'status': 'approved',
        'downloads': 456,
        'upload_date': '2024-01-19',
        'uploader': 'user202',
        'file_size': '2.2 MB',
        'resolution': '1920x1080',
        'category': 'Nature'
    },
    {
        'id': 6,
        'title': 'Space Galaxy',
        'tags': ['space', 'stars', 'galaxy'],
        'status': 'pending',
        'downloads': 123,
        'upload_date': '2024-01-23',
        'uploader': 'user303',
        'file_size': '3.5 MB',
        'resolution': '2560x1440',
        'category': 'Space'
    }
]

@wallpapers_bp.route('/api/wallpapers', methods=['GET'])
def get_wallpapers():
    """Get all wallpapers with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status', 'all')
        search = request.args.get('search', '').lower()
        category = request.args.get('category', 'all')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        
        # Filter wallpapers
        filtered_wallpapers = sample_wallpapers.copy()
        
        # Filter by status
        if status != 'all':
            filtered_wallpapers = [w for w in filtered_wallpapers if w['status'] == status]
        
        # Filter by search term
        if search:
            filtered_wallpapers = [
                w for w in filtered_wallpapers 
                if search in w['title'].lower() or 
                   any(search in tag.lower() for tag in w['tags'])
            ]
        
        # Filter by category
        if category != 'all':
            filtered_wallpapers = [w for w in filtered_wallpapers if w['category'] == category]
        
        # Pagination
        total = len(filtered_wallpapers)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_wallpapers = filtered_wallpapers[start:end]
        
        return jsonify({
            'wallpapers': paginated_wallpapers,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/stats', methods=['GET'])
def get_wallpaper_stats():
    """Get wallpaper statistics"""
    try:
        total = len(sample_wallpapers)
        approved = len([w for w in sample_wallpapers if w['status'] == 'approved'])
        pending = len([w for w in sample_wallpapers if w['status'] == 'pending'])
        flagged = len([w for w in sample_wallpapers if w['status'] == 'flagged'])
        
        return jsonify({
            'total': total,
            'approved': approved,
            'pending': pending,
            'flagged': flagged,
            'total_downloads': sum(w['downloads'] for w in sample_wallpapers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/categories', methods=['GET'])
def get_categories():
    """Get all wallpaper categories"""
    try:
        categories = list(set(w['category'] for w in sample_wallpapers))
        category_stats = {}
        
        for category in categories:
            count = len([w for w in sample_wallpapers if w['category'] == category])
            category_stats[category] = count
        
        return jsonify({
            'categories': categories,
            'stats': category_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/<int:wallpaper_id>', methods=['GET'])
def get_wallpaper(wallpaper_id):
    """Get a specific wallpaper by ID"""
    try:
        wallpaper = next((w for w in sample_wallpapers if w['id'] == wallpaper_id), None)
        if not wallpaper:
            return jsonify({'error': 'Wallpaper not found'}), 404
        
        return jsonify(wallpaper)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/<int:wallpaper_id>/status', methods=['PUT'])
def update_wallpaper_status(wallpaper_id):
    """Update wallpaper status (approve, reject, flag)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['approved', 'pending', 'flagged', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Find and update wallpaper
        for wallpaper in sample_wallpapers:
            if wallpaper['id'] == wallpaper_id:
                wallpaper['status'] = new_status
                return jsonify({
                    'message': f'Wallpaper status updated to {new_status}',
                    'wallpaper': wallpaper
                })
        
        return jsonify({'error': 'Wallpaper not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/<int:wallpaper_id>', methods=['DELETE'])
def delete_wallpaper(wallpaper_id):
    """Delete a wallpaper"""
    try:
        global sample_wallpapers
        original_length = len(sample_wallpapers)
        sample_wallpapers = [w for w in sample_wallpapers if w['id'] != wallpaper_id]
        
        if len(sample_wallpapers) == original_length:
            return jsonify({'error': 'Wallpaper not found'}), 404
        
        return jsonify({'message': 'Wallpaper deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/upload', methods=['POST'])
def upload_wallpaper():
    """Upload a new wallpaper"""
    try:
        # In a real implementation, this would handle file upload
        # For now, we'll simulate the upload process
        
        data = request.get_json()
        title = data.get('title')
        tags = data.get('tags', [])
        category = data.get('category', 'Other')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Create new wallpaper entry
        new_wallpaper = {
            'id': max(w['id'] for w in sample_wallpapers) + 1,
            'title': title,
            'tags': tags,
            'status': 'pending',  # New uploads start as pending
            'downloads': 0,
            'upload_date': datetime.now().strftime('%Y-%m-%d'),
            'uploader': 'current_user',  # In real app, get from auth
            'file_size': f"{random.uniform(1.0, 4.0):.1f} MB",
            'resolution': random.choice(['1920x1080', '2560x1440', '3840x2160']),
            'category': category
        }
        
        sample_wallpapers.append(new_wallpaper)
        
        return jsonify({
            'message': 'Wallpaper uploaded successfully',
            'wallpaper': new_wallpaper
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/<int:wallpaper_id>/tags', methods=['PUT'])
def update_wallpaper_tags(wallpaper_id):
    """Update wallpaper tags"""
    try:
        data = request.get_json()
        new_tags = data.get('tags', [])
        
        # Find and update wallpaper
        for wallpaper in sample_wallpapers:
            if wallpaper['id'] == wallpaper_id:
                wallpaper['tags'] = new_tags
                return jsonify({
                    'message': 'Tags updated successfully',
                    'wallpaper': wallpaper
                })
        
        return jsonify({'error': 'Wallpaper not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallpapers_bp.route('/api/wallpapers/recent', methods=['GET'])
def get_recent_wallpapers():
    """Get recently uploaded wallpapers"""
    try:
        # Sort by upload date (most recent first)
        sorted_wallpapers = sorted(
            sample_wallpapers, 
            key=lambda x: x['upload_date'], 
            reverse=True
        )
        
        # Return top 10 recent wallpapers
        recent_wallpapers = sorted_wallpapers[:10]
        
        return jsonify({
            'wallpapers': recent_wallpapers,
            'count': len(recent_wallpapers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

