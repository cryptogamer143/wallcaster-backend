from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

reports_bp = Blueprint('reports', __name__)

# Mock data for reports
mock_reports = [
    {
        'id': 1,
        'type': 'wallpaper',
        'title': 'Inappropriate Content',
        'target': 'Mountain Landscape',
        'target_id': 'wp_001',
        'reporter': 'user123',
        'reporter_id': 'u_123',
        'status': 'pending',
        'priority': 'high',
        'date': '2024-01-15',
        'created_at': '2024-01-15T10:30:00Z',
        'reason': 'Contains inappropriate content',
        'description': 'This wallpaper contains content that violates our community guidelines.',
        'category': 'inappropriate_content',
        'moderator_notes': '',
        'resolution': '',
        'resolved_at': None,
        'resolved_by': None
    },
    {
        'id': 2,
        'type': 'user',
        'title': 'Spam Behavior',
        'target': 'spammer_user',
        'target_id': 'u_456',
        'reporter': 'user456',
        'reporter_id': 'u_456',
        'status': 'resolved',
        'priority': 'medium',
        'date': '2024-01-14',
        'created_at': '2024-01-14T14:20:00Z',
        'reason': 'User is uploading spam wallpapers',
        'description': 'This user has been consistently uploading low-quality spam content.',
        'category': 'spam',
        'moderator_notes': 'User warned and content removed',
        'resolution': 'User suspended for 7 days',
        'resolved_at': '2024-01-14T16:45:00Z',
        'resolved_by': 'mod_001'
    },
    {
        'id': 3,
        'type': 'wallpaper',
        'title': 'Copyright Violation',
        'target': 'City Skyline',
        'target_id': 'wp_002',
        'reporter': 'user789',
        'reporter_id': 'u_789',
        'status': 'investigating',
        'priority': 'high',
        'date': '2024-01-13',
        'created_at': '2024-01-13T09:15:00Z',
        'reason': 'This appears to be copyrighted material',
        'description': 'The wallpaper appears to be a copyrighted image from a professional photographer.',
        'category': 'copyright',
        'moderator_notes': 'Investigating copyright claim',
        'resolution': '',
        'resolved_at': None,
        'resolved_by': None
    },
    {
        'id': 4,
        'type': 'user',
        'title': 'Harassment',
        'target': 'bad_user',
        'target_id': 'u_789',
        'reporter': 'user101',
        'reporter_id': 'u_101',
        'status': 'investigating',
        'priority': 'high',
        'date': '2024-01-12',
        'created_at': '2024-01-12T11:30:00Z',
        'reason': 'User is harassing other users in comments',
        'description': 'Multiple reports of this user sending threatening messages to other users.',
        'category': 'harassment',
        'moderator_notes': 'Collecting evidence from multiple reports',
        'resolution': '',
        'resolved_at': None,
        'resolved_by': None
    },
    {
        'id': 5,
        'type': 'wallpaper',
        'title': 'Malicious Content',
        'target': 'Suspicious Image',
        'target_id': 'wp_003',
        'reporter': 'user202',
        'reporter_id': 'u_202',
        'status': 'rejected',
        'priority': 'low',
        'date': '2024-01-11',
        'created_at': '2024-01-11T13:45:00Z',
        'reason': 'Image might contain malware',
        'description': 'User claims the image file might be malicious.',
        'category': 'security',
        'moderator_notes': 'False alarm - image is clean',
        'resolution': 'Report rejected after security scan',
        'resolved_at': '2024-01-11T15:20:00Z',
        'resolved_by': 'mod_002'
    }
]

# Mock moderation actions
mock_moderation_actions = [
    {
        'id': 1,
        'type': 'user_suspension',
        'target_type': 'user',
        'target_id': 'u_456',
        'target_name': 'spammer_user',
        'moderator': 'mod_001',
        'moderator_name': 'John Moderator',
        'action': 'suspended',
        'duration': '7 days',
        'reason': 'Spam behavior',
        'date': '2024-01-14T16:45:00Z',
        'status': 'active'
    },
    {
        'id': 2,
        'type': 'content_removal',
        'target_type': 'wallpaper',
        'target_id': 'wp_004',
        'target_name': 'Inappropriate Wallpaper',
        'moderator': 'mod_002',
        'moderator_name': 'Jane Moderator',
        'action': 'removed',
        'duration': 'permanent',
        'reason': 'Inappropriate content',
        'date': '2024-01-13T10:20:00Z',
        'status': 'completed'
    },
    {
        'id': 3,
        'type': 'user_warning',
        'target_type': 'user',
        'target_id': 'u_303',
        'target_name': 'warned_user',
        'moderator': 'mod_001',
        'moderator_name': 'John Moderator',
        'action': 'warned',
        'duration': 'N/A',
        'reason': 'Minor policy violation',
        'date': '2024-01-12T14:30:00Z',
        'status': 'completed'
    }
]

@reports_bp.route('/reports', methods=['GET'])
def get_reports():
    """Get all reports with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status', 'all')
        report_type = request.args.get('type', 'all')
        priority = request.args.get('priority', 'all')
        search = request.args.get('search', '')
        
        # Filter reports
        filtered_reports = mock_reports.copy()
        
        if status != 'all':
            filtered_reports = [r for r in filtered_reports if r['status'] == status]
        
        if report_type != 'all':
            filtered_reports = [r for r in filtered_reports if r['type'] == report_type]
        
        if priority != 'all':
            filtered_reports = [r for r in filtered_reports if r['priority'] == priority]
        
        if search:
            search_lower = search.lower()
            filtered_reports = [r for r in filtered_reports if 
                              search_lower in r['title'].lower() or 
                              search_lower in r['target'].lower() or 
                              search_lower in r['reporter'].lower()]
        
        return jsonify({
            'success': True,
            'reports': filtered_reports,
            'total': len(filtered_reports)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/reports/stats', methods=['GET'])
def get_reports_stats():
    """Get reports statistics"""
    try:
        total_reports = len(mock_reports)
        pending_reports = len([r for r in mock_reports if r['status'] == 'pending'])
        resolved_reports = len([r for r in mock_reports if r['status'] == 'resolved'])
        investigating_reports = len([r for r in mock_reports if r['status'] == 'investigating'])
        rejected_reports = len([r for r in mock_reports if r['status'] == 'rejected'])
        
        # High priority reports
        high_priority = len([r for r in mock_reports if r['priority'] == 'high'])
        
        # Reports by type
        wallpaper_reports = len([r for r in mock_reports if r['type'] == 'wallpaper'])
        user_reports = len([r for r in mock_reports if r['type'] == 'user'])
        
        # Recent reports (last 24 hours)
        recent_reports = len([r for r in mock_reports if r['date'] >= '2024-01-14'])
        
        return jsonify({
            'success': True,
            'stats': {
                'total_reports': total_reports,
                'pending_reports': pending_reports,
                'resolved_reports': resolved_reports,
                'investigating_reports': investigating_reports,
                'rejected_reports': rejected_reports,
                'high_priority': high_priority,
                'wallpaper_reports': wallpaper_reports,
                'user_reports': user_reports,
                'recent_reports': recent_reports
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/reports/<int:report_id>', methods=['GET'])
def get_report_details(report_id):
    """Get detailed information about a specific report"""
    try:
        report = next((r for r in mock_reports if r['id'] == report_id), None)
        
        if not report:
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/reports/<int:report_id>/status', methods=['PUT'])
def update_report_status(report_id):
    """Update the status of a report"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        moderator_notes = data.get('moderator_notes', '')
        resolution = data.get('resolution', '')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        # Find and update the report
        for report in mock_reports:
            if report['id'] == report_id:
                report['status'] = new_status
                report['moderator_notes'] = moderator_notes
                report['resolution'] = resolution
                
                if new_status in ['resolved', 'rejected']:
                    report['resolved_at'] = datetime.now().isoformat() + 'Z'
                    report['resolved_by'] = 'mod_001'  # Mock moderator ID
                
                return jsonify({
                    'success': True,
                    'message': 'Report status updated successfully',
                    'report': report
                })
        
        return jsonify({
            'success': False,
            'error': 'Report not found'
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/moderation/actions', methods=['GET'])
def get_moderation_actions():
    """Get moderation actions history"""
    try:
        # Get query parameters
        action_type = request.args.get('type', 'all')
        target_type = request.args.get('target_type', 'all')
        moderator = request.args.get('moderator', 'all')
        
        # Filter actions
        filtered_actions = mock_moderation_actions.copy()
        
        if action_type != 'all':
            filtered_actions = [a for a in filtered_actions if a['type'] == action_type]
        
        if target_type != 'all':
            filtered_actions = [a for a in filtered_actions if a['target_type'] == target_type]
        
        if moderator != 'all':
            filtered_actions = [a for a in filtered_actions if a['moderator'] == moderator]
        
        return jsonify({
            'success': True,
            'actions': filtered_actions,
            'total': len(filtered_actions)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/moderation/actions', methods=['POST'])
def create_moderation_action():
    """Create a new moderation action"""
    try:
        data = request.get_json()
        
        # Create new action
        new_action = {
            'id': len(mock_moderation_actions) + 1,
            'type': data.get('type'),
            'target_type': data.get('target_type'),
            'target_id': data.get('target_id'),
            'target_name': data.get('target_name'),
            'moderator': 'mod_001',  # Mock current moderator
            'moderator_name': 'Current Moderator',
            'action': data.get('action'),
            'duration': data.get('duration', 'N/A'),
            'reason': data.get('reason'),
            'date': datetime.now().isoformat() + 'Z',
            'status': 'active'
        }
        
        mock_moderation_actions.append(new_action)
        
        return jsonify({
            'success': True,
            'message': 'Moderation action created successfully',
            'action': new_action
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@reports_bp.route('/moderation/quick-actions', methods=['POST'])
def quick_moderation_action():
    """Perform quick moderation actions"""
    try:
        data = request.get_json()
        action_type = data.get('action')
        target_type = data.get('target_type')
        target_id = data.get('target_id')
        reason = data.get('reason', 'Quick moderation action')
        
        # Simulate the action
        action_messages = {
            'suspend_user': f'User {target_id} has been suspended',
            'ban_user': f'User {target_id} has been banned',
            'remove_content': f'Content {target_id} has been removed',
            'warn_user': f'User {target_id} has been warned'
        }
        
        message = action_messages.get(action_type, 'Action completed')
        
        return jsonify({
            'success': True,
            'message': message
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

