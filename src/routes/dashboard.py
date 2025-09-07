from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get main dashboard statistics"""
    stats = {
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
    return jsonify(stats)

@dashboard_bp.route('/user-growth', methods=['GET'])
def get_user_growth():
    """Get user growth data for charts"""
    data = [
        {'month': 'Jan', 'users': 8500},
        {'month': 'Feb', 'users': 9200},
        {'month': 'Mar', 'users': 10100},
        {'month': 'Apr', 'users': 10800},
        {'month': 'May', 'users': 11500},
        {'month': 'Jun', 'users': 12543}
    ]
    return jsonify(data)

@dashboard_bp.route('/revenue-trends', methods=['GET'])
def get_revenue_trends():
    """Get revenue trends data for charts"""
    data = [
        {'month': 'Jan', 'revenue': 2800},
        {'month': 'Feb', 'revenue': 3200},
        {'month': 'Mar', 'revenue': 3600},
        {'month': 'Apr', 'revenue': 3900},
        {'month': 'May', 'revenue': 4100},
        {'month': 'Jun', 'revenue': 4231}
    ]
    return jsonify(data)

@dashboard_bp.route('/category-distribution', methods=['GET'])
def get_category_distribution():
    """Get wallpaper category distribution"""
    data = [
        {'name': 'Nature', 'value': 35, 'color': '#1A73E8'},
        {'name': 'Abstract', 'value': 25, 'color': '#28a745'},
        {'name': 'City', 'value': 20, 'color': '#ffc107'},
        {'name': 'Space', 'value': 12, 'color': '#dc3545'},
        {'name': 'Other', 'value': 8, 'color': '#6f42c1'}
    ]
    return jsonify(data)

@dashboard_bp.route('/daily-active', methods=['GET'])
def get_daily_active():
    """Get daily active users for the week"""
    data = [
        {'day': 'Mon', 'active': 2800},
        {'day': 'Tue', 'active': 3200},
        {'day': 'Wed', 'active': 3100},
        {'day': 'Thu', 'active': 3400},
        {'day': 'Fri', 'active': 3600},
        {'day': 'Sat', 'active': 3200},
        {'day': 'Sun', 'active': 3456}
    ]
    return jsonify(data)

@dashboard_bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    """Get recent activity feed"""
    activities = [
        {
            'id': 1,
            'action': 'New wallpaper uploaded',
            'user': 'user123',
            'time': '2 minutes ago',
            'type': 'upload'
        },
        {
            'id': 2,
            'action': 'User reported content',
            'user': 'user456',
            'time': '5 minutes ago',
            'type': 'report'
        },
        {
            'id': 3,
            'action': 'Ad revenue milestone reached',
            'user': 'system',
            'time': '1 hour ago',
            'type': 'milestone'
        },
        {
            'id': 4,
            'action': 'New user registered',
            'user': 'user789',
            'time': '2 hours ago',
            'type': 'user'
        },
        {
            'id': 5,
            'action': 'Wallpaper approved by moderator',
            'user': 'admin',
            'time': '3 hours ago',
            'type': 'moderation'
        }
    ]
    return jsonify(activities)

