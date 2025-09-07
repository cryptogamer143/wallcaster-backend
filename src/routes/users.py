from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json

users_bp = Blueprint('users', __name__)

# Mock user data for development
mock_users = [
    {
        'id': 1,
        'username': 'john_doe',
        'name': 'John Doe',
        'email': 'john@example.com',
        'status': 'active',
        'role': 'user',
        'joinDate': '2024-01-15',
        'createdAt': '2024-01-15T10:00:00Z',
        'lastActive': '2024-09-05T14:30:00Z',
        'wallpapers': 23,
        'reports': 0,
        'recentActivity': [
            {'action': 'Uploaded wallpaper "Mountain Sunset"', 'timestamp': '2024-09-05 14:30'},
            {'action': 'Updated profile', 'timestamp': '2024-09-04 09:15'}
        ]
    },
    {
        'id': 2,
        'username': 'jane_smith',
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'status': 'active',
        'role': 'moderator',
        'joinDate': '2024-01-20',
        'createdAt': '2024-01-20T10:00:00Z',
        'lastActive': '2024-09-06T10:15:00Z',
        'wallpapers': 45,
        'reports': 1,
        'recentActivity': [
            {'action': 'Moderated 5 wallpapers', 'timestamp': '2024-09-06 10:15'},
            {'action': 'Uploaded wallpaper "City Lights"', 'timestamp': '2024-09-05 16:45'}
        ]
    },
    {
        'id': 3,
        'username': 'mike_wilson',
        'name': 'Mike Wilson',
        'email': 'mike@example.com',
        'status': 'banned',
        'role': 'user',
        'joinDate': '2024-01-10',
        'createdAt': '2024-01-10T10:00:00Z',
        'lastActive': '2024-08-15T12:00:00Z',
        'wallpapers': 12,
        'reports': 5,
        'recentActivity': [
            {'action': 'Account banned for policy violations', 'timestamp': '2024-08-15 12:00'},
            {'action': 'Received warning for inappropriate content', 'timestamp': '2024-08-10 14:30'}
        ]
    },
    {
        'id': 4,
        'username': 'sarah_jones',
        'name': 'Sarah Jones',
        'email': 'sarah@example.com',
        'status': 'active',
        'role': 'admin',
        'joinDate': '2024-01-25',
        'createdAt': '2024-01-25T10:00:00Z',
        'lastActive': '2024-09-06T11:00:00Z',
        'wallpapers': 67,
        'reports': 0,
        'recentActivity': [
            {'action': 'Reviewed moderation queue', 'timestamp': '2024-09-06 11:00'},
            {'action': 'Updated system settings', 'timestamp': '2024-09-06 09:30'}
        ]
    },
    {
        'id': 5,
        'username': 'alex_brown',
        'name': 'Alex Brown',
        'email': 'alex@example.com',
        'status': 'suspended',
        'role': 'user',
        'joinDate': '2024-01-18',
        'createdAt': '2024-01-18T10:00:00Z',
        'lastActive': '2024-08-20T15:45:00Z',
        'wallpapers': 34,
        'reports': 3,
        'recentActivity': [
            {'action': 'Account suspended for 30 days', 'timestamp': '2024-08-20 15:45'},
            {'action': 'Uploaded wallpaper "Abstract Art"', 'timestamp': '2024-08-19 12:30'}
        ]
    },
    {
        'id': 6,
        'username': 'emma_davis',
        'name': 'Emma Davis',
        'email': 'emma@example.com',
        'status': 'active',
        'role': 'user',
        'joinDate': '2024-09-06',
        'createdAt': '2024-09-06T08:00:00Z',
        'lastActive': '2024-09-06T12:00:00Z',
        'wallpapers': 2,
        'reports': 0,
        'recentActivity': [
            {'action': 'Joined WallCaster', 'timestamp': '2024-09-06 08:00'},
            {'action': 'Uploaded first wallpaper', 'timestamp': '2024-09-06 10:30'}
        ]
    }
]

@users_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users with optional filtering and searching"""
    try:
        # Get query parameters
        search = request.args.get('search', '').lower()
        status_filter = request.args.get('status', 'all')
        role_filter = request.args.get('role', 'all')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # Filter users
        filtered_users = mock_users.copy()
        
        if search:
            filtered_users = [
                user for user in filtered_users
                if search in user['name'].lower() or 
                   search in user['email'].lower() or 
                   search in user['username'].lower()
            ]
        
        if status_filter != 'all':
            filtered_users = [user for user in filtered_users if user['status'] == status_filter]
        
        if role_filter != 'all':
            filtered_users = [user for user in filtered_users if user['role'] == role_filter]
        
        # Pagination
        start = (page - 1) * per_page
        end = start + per_page
        paginated_users = filtered_users[start:end]
        
        return jsonify({
            'users': paginated_users,
            'total': len(filtered_users),
            'page': page,
            'per_page': per_page,
            'pages': (len(filtered_users) + per_page - 1) // per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics"""
    try:
        total = len(mock_users)
        active = len([u for u in mock_users if u['status'] == 'active'])
        suspended = len([u for u in mock_users if u['status'] == 'suspended'])
        banned = len([u for u in mock_users if u['status'] == 'banned'])
        pending = len([u for u in mock_users if u['status'] == 'pending'])
        
        # Calculate new users today
        today = datetime.now().date()
        new_today = len([
            u for u in mock_users 
            if datetime.fromisoformat(u['createdAt'].replace('Z', '+00:00')).date() == today
        ])
        
        return jsonify({
            'total': total,
            'active': active,
            'suspended': suspended,
            'banned': banned,
            'pending': pending,
            'newToday': new_today
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = next((u for u in mock_users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """Update user role"""
    try:
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['user', 'moderator', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Find and update user
        user = next((u for u in mock_users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        old_role = user['role']
        user['role'] = new_role
        
        # Add to recent activity
        user['recentActivity'].insert(0, {
            'action': f'Role changed from {old_role} to {new_role}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        
        # Keep only last 10 activities
        user['recentActivity'] = user['recentActivity'][:10]
        
        return jsonify({
            'message': 'User role updated successfully',
            'user': user
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>/status', methods=['PUT'])
def update_user_status(user_id):
    """Update user status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['active', 'suspended', 'banned', 'pending']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Find and update user
        user = next((u for u in mock_users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        old_status = user['status']
        user['status'] = new_status
        
        # Update last active if status is being set to active
        if new_status == 'active':
            user['lastActive'] = datetime.now().isoformat() + 'Z'
        
        # Add to recent activity
        user['recentActivity'].insert(0, {
            'action': f'Status changed from {old_status} to {new_status}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        
        # Keep only last 10 activities
        user['recentActivity'] = user['recentActivity'][:10]
        
        return jsonify({
            'message': 'User status updated successfully',
            'user': user
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if username or email already exists
        if any(u['username'] == data['username'] for u in mock_users):
            return jsonify({'error': 'Username already exists'}), 400
        
        if any(u['email'] == data['email'] for u in mock_users):
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = {
            'id': max(u['id'] for u in mock_users) + 1,
            'username': data['username'],
            'name': data['name'],
            'email': data['email'],
            'status': data.get('status', 'active'),
            'role': data.get('role', 'user'),
            'joinDate': datetime.now().strftime('%Y-%m-%d'),
            'createdAt': datetime.now().isoformat() + 'Z',
            'lastActive': datetime.now().isoformat() + 'Z',
            'wallpapers': 0,
            'reports': 0,
            'recentActivity': [
                {
                    'action': 'Account created',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        }
        
        mock_users.append(new_user)
        
        return jsonify({
            'message': 'User created successfully',
            'user': new_user
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        
        # Find user
        user = next((u for u in mock_users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['name', 'email', 'username']
        updated_fields = []
        
        for field in allowed_fields:
            if field in data and data[field] != user[field]:
                # Check for duplicates
                if field in ['username', 'email']:
                    if any(u['id'] != user_id and u[field] == data[field] for u in mock_users):
                        return jsonify({'error': f'{field.capitalize()} already exists'}), 400
                
                user[field] = data[field]
                updated_fields.append(field)
        
        if updated_fields:
            # Add to recent activity
            user['recentActivity'].insert(0, {
                'action': f'Updated {", ".join(updated_fields)}',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            
            # Keep only last 10 activities
            user['recentActivity'] = user['recentActivity'][:10]
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        # Find user
        user_index = next((i for i, u in enumerate(mock_users) if u['id'] == user_id), None)
        
        if user_index is None:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove user
        deleted_user = mock_users.pop(user_index)
        
        return jsonify({
            'message': 'User deleted successfully',
            'user': deleted_user
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>/activity', methods=['GET'])
def get_user_activity(user_id):
    """Get user activity history"""
    try:
        user = next((u for u in mock_users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'userId': user_id,
            'activity': user.get('recentActivity', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/recent', methods=['GET'])
def get_recent_users():
    """Get recently joined users"""
    try:
        # Sort users by creation date (most recent first)
        sorted_users = sorted(
            mock_users, 
            key=lambda u: datetime.fromisoformat(u['createdAt'].replace('Z', '+00:00')), 
            reverse=True
        )
        
        # Return top 10 recent users
        recent_users = sorted_users[:10]
        
        return jsonify({
            'users': recent_users,
            'total': len(recent_users)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

