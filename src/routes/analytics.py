from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

analytics_bp = Blueprint('analytics', __name__)

# Mock data generators for analytics
def generate_daily_active_users(days=30):
    """Generate mock daily active users data"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_users = 3000
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        # Add some realistic variation
        variation = random.uniform(0.8, 1.2)
        trend = 1 + (i * 0.01)  # Slight upward trend
        users = int(base_users * variation * trend)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'users': users,
            'new_users': int(users * 0.15),
            'returning_users': int(users * 0.85)
        })
    
    return data

def generate_download_trends(days=30):
    """Generate mock download trends data"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_downloads = 2500
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        variation = random.uniform(0.7, 1.3)
        trend = 1 + (i * 0.008)
        downloads = int(base_downloads * variation * trend)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'downloads': downloads,
            'premium_downloads': int(downloads * 0.25),
            'free_downloads': int(downloads * 0.75)
        })
    
    return data

def generate_revenue_data(days=30):
    """Generate mock revenue data"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_revenue = 150
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        variation = random.uniform(0.8, 1.4)
        trend = 1 + (i * 0.012)
        revenue = base_revenue * variation * trend
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': round(revenue, 2),
            'ad_revenue': round(revenue * 0.6, 2),
            'premium_revenue': round(revenue * 0.4, 2)
        })
    
    return data

# Mock data
TOP_WALLPAPERS = [
    {
        'id': 1,
        'title': 'Mountain Landscape 4K',
        'downloads': 15432,
        'views': 45678,
        'revenue': 234.56,
        'category': 'Nature',
        'upload_date': '2024-08-15',
        'rating': 4.8,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 2,
        'title': 'Ocean Waves Sunset',
        'downloads': 12876,
        'views': 38945,
        'revenue': 198.43,
        'category': 'Nature',
        'upload_date': '2024-08-20',
        'rating': 4.7,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 3,
        'title': 'City Skyline Night',
        'downloads': 11234,
        'views': 34567,
        'revenue': 176.89,
        'category': 'Urban',
        'upload_date': '2024-08-18',
        'rating': 4.6,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 4,
        'title': 'Forest Path Autumn',
        'downloads': 9876,
        'views': 29876,
        'revenue': 154.32,
        'category': 'Nature',
        'upload_date': '2024-08-22',
        'rating': 4.5,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 5,
        'title': 'Desert Sunset Dunes',
        'downloads': 8765,
        'views': 26543,
        'revenue': 132.45,
        'category': 'Nature',
        'upload_date': '2024-08-25',
        'rating': 4.4,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 6,
        'title': 'Space Galaxy Stars',
        'downloads': 7654,
        'views': 23456,
        'revenue': 118.76,
        'category': 'Space',
        'upload_date': '2024-08-28',
        'rating': 4.3,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 7,
        'title': 'Minimalist Abstract',
        'downloads': 6543,
        'views': 19876,
        'revenue': 98.65,
        'category': 'Abstract',
        'upload_date': '2024-08-30',
        'rating': 4.2,
        'thumbnail': '/api/placeholder/150/100'
    },
    {
        'id': 8,
        'title': 'Tropical Beach Paradise',
        'downloads': 5432,
        'views': 16789,
        'revenue': 87.54,
        'category': 'Nature',
        'upload_date': '2024-09-01',
        'rating': 4.1,
        'thumbnail': '/api/placeholder/150/100'
    }
]

AD_PERFORMANCE_DATA = [
    {
        'type': 'Search Ads',
        'impressions': 125678,
        'clicks': 5234,
        'revenue': 1876.43,
        'ctr': 4.16,
        'cpm': 14.92,
        'conversion_rate': 2.8
    },
    {
        'type': '4K Unlock Ads',
        'impressions': 89456,
        'clicks': 3876,
        'revenue': 1543.21,
        'ctr': 4.33,
        'cpm': 17.25,
        'conversion_rate': 3.2
    },
    {
        'type': 'Banner Ads',
        'impressions': 156789,
        'clicks': 4567,
        'revenue': 987.65,
        'ctr': 2.91,
        'cpm': 6.30,
        'conversion_rate': 1.5
    },
    {
        'type': 'Video Ads',
        'impressions': 67890,
        'clicks': 2345,
        'revenue': 1234.56,
        'ctr': 3.45,
        'cpm': 18.18,
        'conversion_rate': 4.1
    },
    {
        'type': 'Native Ads',
        'impressions': 98765,
        'clicks': 3456,
        'revenue': 765.43,
        'ctr': 3.50,
        'cpm': 7.75,
        'conversion_rate': 2.1
    }
]

@analytics_bp.route('/api/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get analytics overview with key metrics"""
    try:
        # Calculate totals from recent data
        daily_users = generate_daily_active_users(7)
        downloads = generate_download_trends(7)
        revenue = generate_revenue_data(7)
        
        current_dau = daily_users[-1]['users']
        previous_dau = daily_users[-2]['users']
        dau_change = ((current_dau - previous_dau) / previous_dau) * 100
        
        total_downloads = sum([d['downloads'] for d in downloads])
        prev_downloads = sum([d['downloads'] for d in downloads[:-1]])
        downloads_change = ((total_downloads - prev_downloads) / prev_downloads) * 100 if prev_downloads > 0 else 0
        
        total_revenue = sum([r['revenue'] for r in revenue])
        prev_revenue = sum([r['revenue'] for r in revenue[:-1]])
        revenue_change = ((total_revenue - prev_revenue) / prev_revenue) * 100 if prev_revenue > 0 else 0
        
        total_views = sum([w['views'] for w in TOP_WALLPAPERS])
        
        overview = {
            'daily_active_users': {
                'current': current_dau,
                'change': round(dau_change, 1),
                'trend': 'up' if dau_change > 0 else 'down'
            },
            'total_downloads': {
                'current': total_downloads,
                'change': round(downloads_change, 1),
                'trend': 'up' if downloads_change > 0 else 'down'
            },
            'page_views': {
                'current': total_views,
                'change': 15.3,
                'trend': 'up'
            },
            'ad_revenue': {
                'current': round(total_revenue, 2),
                'change': round(revenue_change, 1),
                'trend': 'up' if revenue_change > 0 else 'down'
            }
        }
        
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/user-activity', methods=['GET'])
def get_user_activity():
    """Get user activity trends"""
    try:
        days = request.args.get('days', 30, type=int)
        data = generate_daily_active_users(days)
        
        return jsonify({
            'data': data,
            'total_days': days,
            'average_dau': sum([d['users'] for d in data]) // len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/download-trends', methods=['GET'])
def get_download_trends():
    """Get download trends"""
    try:
        days = request.args.get('days', 30, type=int)
        data = generate_download_trends(days)
        
        return jsonify({
            'data': data,
            'total_days': days,
            'total_downloads': sum([d['downloads'] for d in data])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/revenue-trends', methods=['GET'])
def get_revenue_trends():
    """Get revenue trends"""
    try:
        days = request.args.get('days', 30, type=int)
        data = generate_revenue_data(days)
        
        return jsonify({
            'data': data,
            'total_days': days,
            'total_revenue': sum([d['revenue'] for d in data])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/top-wallpapers', methods=['GET'])
def get_top_wallpapers():
    """Get top performing wallpapers"""
    try:
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category', None)
        
        wallpapers = TOP_WALLPAPERS.copy()
        
        if category and category != 'all':
            wallpapers = [w for w in wallpapers if w['category'].lower() == category.lower()]
        
        # Sort by downloads and limit results
        wallpapers = sorted(wallpapers, key=lambda x: x['downloads'], reverse=True)[:limit]
        
        # Add calculated metrics
        for wallpaper in wallpapers:
            wallpaper['conversion_rate'] = round((wallpaper['downloads'] / wallpaper['views']) * 100, 2)
            wallpaper['revenue_per_download'] = round(wallpaper['revenue'] / wallpaper['downloads'], 3)
        
        return jsonify({
            'wallpapers': wallpapers,
            'total_count': len(wallpapers),
            'categories': list(set([w['category'] for w in TOP_WALLPAPERS]))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/ad-performance', methods=['GET'])
def get_ad_performance():
    """Get ad performance metrics"""
    try:
        ad_data = AD_PERFORMANCE_DATA.copy()
        
        # Calculate additional metrics
        for ad in ad_data:
            ad['ctr'] = round((ad['clicks'] / ad['impressions']) * 100, 2)
            ad['cpm'] = round((ad['revenue'] / ad['impressions']) * 1000, 2)
            ad['revenue_per_click'] = round(ad['revenue'] / ad['clicks'], 3)
        
        # Calculate totals
        totals = {
            'total_impressions': sum([ad['impressions'] for ad in ad_data]),
            'total_clicks': sum([ad['clicks'] for ad in ad_data]),
            'total_revenue': sum([ad['revenue'] for ad in ad_data]),
            'average_ctr': sum([ad['ctr'] for ad in ad_data]) / len(ad_data),
            'average_cpm': sum([ad['cpm'] for ad in ad_data]) / len(ad_data)
        }
        
        return jsonify({
            'ad_performance': ad_data,
            'totals': totals
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/category-performance', methods=['GET'])
def get_category_performance():
    """Get performance by wallpaper category"""
    try:
        categories = {}
        
        for wallpaper in TOP_WALLPAPERS:
            category = wallpaper['category']
            if category not in categories:
                categories[category] = {
                    'category': category,
                    'wallpapers': 0,
                    'total_downloads': 0,
                    'total_views': 0,
                    'total_revenue': 0,
                    'average_rating': 0
                }
            
            categories[category]['wallpapers'] += 1
            categories[category]['total_downloads'] += wallpaper['downloads']
            categories[category]['total_views'] += wallpaper['views']
            categories[category]['total_revenue'] += wallpaper['revenue']
            categories[category]['average_rating'] += wallpaper['rating']
        
        # Calculate averages and conversion rates
        category_list = []
        for category_data in categories.values():
            category_data['average_rating'] = round(category_data['average_rating'] / category_data['wallpapers'], 2)
            category_data['conversion_rate'] = round((category_data['total_downloads'] / category_data['total_views']) * 100, 2)
            category_data['revenue_per_wallpaper'] = round(category_data['total_revenue'] / category_data['wallpapers'], 2)
            category_list.append(category_data)
        
        # Sort by total downloads
        category_list = sorted(category_list, key=lambda x: x['total_downloads'], reverse=True)
        
        return jsonify({
            'categories': category_list,
            'total_categories': len(category_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

