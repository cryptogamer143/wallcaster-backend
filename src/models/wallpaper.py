from datetime import datetime
from .user import db

class Wallpaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail_filename = db.Column(db.String(255))
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.Text)  # JSON string of tags
    resolution = db.Column(db.String(50))  # e.g., "1920x1080"
    file_size = db.Column(db.Integer)  # in bytes
    downloads = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    featured = db.Column(db.Boolean, default=False)
    premium = db.Column(db.Boolean, default=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    uploader = db.relationship('User', backref=db.backref('wallpapers', lazy=True))
    
    def __repr__(self):
        return f'<Wallpaper {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'thumbnail_filename': self.thumbnail_filename,
            'category': self.category,
            'tags': self.tags,
            'resolution': self.resolution,
            'file_size': self.file_size,
            'downloads': self.downloads,
            'views': self.views,
            'likes': self.likes,
            'status': self.status,
            'featured': self.featured,
            'premium': self.premium,
            'uploaded_by': self.uploaded_by,
            'uploader': self.uploader.username if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

