"""
Seed script to populate the database with sample data
"""
import os
import sys
import random
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.user import db, User
from src.models.wallpaper import Wallpaper
from src.models.report import Report
from src.models.analytics import AnalyticsEvent, AdPerformance

def create_sample_users():
    """Create sample users"""
    users = [
        {
            'username': 'admin',
            'email': 'admin@wallcaster.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'status': 'active',
            'email_verified': True
        },
        {
            'username': 'moderator',
            'email': 'mod@wallcaster.com',
            'password': 'mod123',
            'first_name': 'Moderator',
            'last_name': 'User',
            'role': 'moderator',
            'status': 'active',
            'email_verified': True
        },
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'user123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'user',
            'status': 'active',
            'email_verified': True
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'user123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'user',
            'status': 'active',
            'email_verified': True
        },
        {
            'username': 'mike_wilson',
            'email': 'mike@example.com',
            'password': 'user123',
            'first_name': 'Mike',
            'last_name': 'Wilson',
            'role': 'user',
            'status': 'active',
            'email_verified': False
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role'],
                status=user_data['status'],
                email_verified=user_data['email_verified']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            created_users.append(user)
        else:
            created_users.append(existing_user)
    
    db.session.commit()
    return created_users

def create_sample_wallpapers(users):
    """Create sample wallpapers"""
    categories = ['Nature', 'Urban', 'Abstract', 'Space', 'Animals', 'Technology']
    statuses = ['approved', 'pending', 'rejected']
    
    wallpapers_data = [
        {
            'title': 'Sunset Mountains',
            'description': 'Beautiful mountain sunset wallpaper with vibrant colors',
            'category': 'Nature',
            'tags': '["sunset", "mountains", "landscape", "nature"]',
            'resolution': '1920x1080',
            'file_size': 2048000,
            'status': 'approved',
            'featured': True,
            'premium': False
        },
        {
            'title': 'Ocean Waves',
            'description': 'Calming ocean waves with crystal clear water',
            'category': 'Nature',
            'tags': '["ocean", "waves", "blue", "water"]',
            'resolution': '2560x1440',
            'file_size': 3072000,
            'status': 'approved',
            'featured': False,
            'premium': True
        },
        {
            'title': 'City Skyline',
            'description': 'Modern city skyline at night with bright lights',
            'category': 'Urban',
            'tags': '["city", "skyline", "night", "lights"]',
            'resolution': '3840x2160',
            'file_size': 5120000,
            'status': 'approved',
            'featured': True,
            'premium': False
        },
        {
            'title': 'Abstract Art',
            'description': 'Colorful abstract digital art with geometric patterns',
            'category': 'Abstract',
            'tags': '["abstract", "colorful", "digital", "art"]',
            'resolution': '1920x1080',
            'file_size': 1536000,
            'status': 'pending',
            'featured': False,
            'premium': False
        },
        {
            'title': 'Space Galaxy',
            'description': 'Deep space galaxy with stars and nebula',
            'category': 'Space',
            'tags': '["space", "galaxy", "stars", "nebula"]',
            'resolution': '2560x1440',
            'file_size': 4096000,
            'status': 'approved',
            'featured': True,
            'premium': True
        },
        {
            'title': 'Forest Path',
            'description': 'Peaceful forest path with green trees',
            'category': 'Nature',
            'tags': '["forest", "path", "green", "trees"]',
            'resolution': '1920x1080',
            'file_size': 2560000,
            'status': 'approved',
            'featured': False,
            'premium': False
        }
    ]
    
    created_wallpapers = []
    for i, wallpaper_data in enumerate(wallpapers_data):
        wallpaper = Wallpaper(
            title=wallpaper_data['title'],
            description=wallpaper_data['description'],
            filename=f'sample_{i+1}.jpg',
            thumbnail_filename=f'thumb_sample_{i+1}.jpg',
            category=wallpaper_data['category'],
            tags=wallpaper_data['tags'],
            resolution=wallpaper_data['resolution'],
            file_size=wallpaper_data['file_size'],
            downloads=random.randint(100, 2000),
            views=random.randint(500, 5000),
            likes=random.randint(10, 500),
            status=wallpaper_data['status'],
            featured=wallpaper_data['featured'],
            premium=wallpaper_data['premium'],
            uploaded_by=random.choice(users).id,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        db.session.add(wallpaper)
        created_wallpapers.append(wallpaper)
    
    db.session.commit()
    return created_wallpapers

def create_sample_analytics(users, wallpapers):
    """Create sample analytics events"""
    event_types = ['view', 'download', 'like', 'search']
    
    # Create events for the last 30 days
    for day in range(30):
        date = datetime.utcnow() - timedelta(days=day)
        
        # Create random events for this day
        for _ in range(random.randint(50, 200)):
            event = AnalyticsEvent(
                event_type=random.choice(event_types),
                wallpaper_id=random.choice(wallpapers).id if random.choice([True, False]) else None,
                user_id=random.choice(users).id if random.choice([True, False]) else None,
                session_id=f'session_{random.randint(1000, 9999)}',
                ip_address=f'192.168.1.{random.randint(1, 255)}',
                created_at=date
            )
            db.session.add(event)
    
    db.session.commit()

def create_sample_ad_performance():
    """Create sample ad performance data"""
    ad_types = ['banner', 'interstitial', 'video', 'native']
    
    for day in range(30):
        date = (datetime.utcnow() - timedelta(days=day)).date()
        
        for i in range(5):  # 5 different ads
            ad_performance = AdPerformance(
                ad_id=f'ad_{i+1}',
                ad_name=f'Ad Campaign {i+1}',
                ad_type=random.choice(ad_types),
                impressions=random.randint(1000, 10000),
                clicks=random.randint(10, 500),
                revenue=round(random.uniform(10.0, 100.0), 2),
                date=date
            )
            db.session.add(ad_performance)
    
    db.session.commit()

def seed_database():
    """Main function to seed the database"""
    print("Creating sample users...")
    users = create_sample_users()
    
    print("Creating sample wallpapers...")
    wallpapers = create_sample_wallpapers(users)
    
    print("Creating sample analytics events...")
    create_sample_analytics(users, wallpapers)
    
    print("Creating sample ad performance data...")
    create_sample_ad_performance()
    
    print("Database seeded successfully!")

if __name__ == '__main__':
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        seed_database()

