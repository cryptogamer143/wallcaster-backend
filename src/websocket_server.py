from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users and their rooms
connected_users = {}
admin_rooms = ['admin_dashboard', 'wallpaper_updates', 'user_activity', 'reports_updates']

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('connection_status', {'status': 'connected', 'timestamp': datetime.utcnow().isoformat()})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    # Clean up user from rooms
    if request.sid in connected_users:
        del connected_users[request.sid]

@socketio.on('join_admin')
def handle_join_admin(data):
    """Join admin rooms for real-time updates"""
    user_id = data.get('user_id')
    user_role = data.get('role', 'user')
    
    if user_role in ['admin', 'moderator']:
        connected_users[request.sid] = {
            'user_id': user_id,
            'role': user_role,
            'joined_at': datetime.utcnow().isoformat()
        }
        
        # Join all admin rooms
        for room in admin_rooms:
            join_room(room)
        
        emit('admin_joined', {
            'rooms': admin_rooms,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Send initial dashboard stats
        emit('dashboard_update', get_dashboard_stats())

@socketio.on('leave_admin')
def handle_leave_admin():
    """Leave admin rooms"""
    for room in admin_rooms:
        leave_room(room)
    
    if request.sid in connected_users:
        del connected_users[request.sid]
    
    emit('admin_left', {'timestamp': datetime.utcnow().isoformat()})

# Real-time event broadcasters
def broadcast_wallpaper_update(wallpaper_data, action='update'):
    """Broadcast wallpaper updates to admin users"""
    socketio.emit('wallpaper_update', {
        'action': action,  # 'create', 'update', 'delete', 'status_change'
        'wallpaper': wallpaper_data,
        'timestamp': datetime.utcnow().isoformat()
    }, room='wallpaper_updates')

def broadcast_user_activity(activity_data):
    """Broadcast user activity to admin users"""
    socketio.emit('user_activity', {
        'activity': activity_data,
        'timestamp': datetime.utcnow().isoformat()
    }, room='user_activity')

def broadcast_report_update(report_data, action='update'):
    """Broadcast report updates to admin users"""
    socketio.emit('report_update', {
        'action': action,  # 'create', 'update', 'resolve', 'reject'
        'report': report_data,
        'timestamp': datetime.utcnow().isoformat()
    }, room='reports_updates')

def broadcast_dashboard_stats(stats_data):
    """Broadcast dashboard statistics updates"""
    socketio.emit('dashboard_update', {
        'stats': stats_data,
        'timestamp': datetime.utcnow().isoformat()
    }, room='admin_dashboard')

def get_dashboard_stats():
    """Get current dashboard statistics"""
    # This would normally fetch from database
    return {
        'totalUsers': 12543,
        'totalWallpapers': 8921,
        'adRevenue': 4231,
        'dailyActive': 3456,
        'changes': {
            'users': '+12%',
            'wallpapers': '+8%',
            'revenue': '+23%',
            'active': '+5%'
        }
    }

# Test endpoints for triggering real-time updates
@app.route('/test/wallpaper-update')
def test_wallpaper_update():
    test_wallpaper = {
        'id': 123,
        'title': 'Test Wallpaper',
        'status': 'approved',
        'downloads': 1500
    }
    broadcast_wallpaper_update(test_wallpaper, 'status_change')
    return {'message': 'Wallpaper update broadcasted'}

@app.route('/test/user-activity')
def test_user_activity():
    test_activity = {
        'user_id': 456,
        'username': 'testuser',
        'action': 'downloaded_wallpaper',
        'target': 'Mountain Landscape'
    }
    broadcast_user_activity(test_activity)
    return {'message': 'User activity broadcasted'}

@app.route('/test/dashboard-stats')
def test_dashboard_stats():
    stats = get_dashboard_stats()
    broadcast_dashboard_stats(stats)
    return {'message': 'Dashboard stats broadcasted'}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)

