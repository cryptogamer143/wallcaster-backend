from datetime import datetime
from .user import db

class AnalyticsEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # download, view, like, search, etc.
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpaper.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    event_metadata = db.Column(db.Text)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wallpaper = db.relationship('Wallpaper', backref=db.backref('analytics_events', lazy=True))
    user = db.relationship('User', backref=db.backref('analytics_events', lazy=True))
    
    def __repr__(self):
        return f'<AnalyticsEvent {self.event_type} - {self.created_at}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'wallpaper_id': self.wallpaper_id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'event_metadata': self.event_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AdPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.String(100), nullable=False)
    ad_name = db.Column(db.String(200), nullable=False)
    ad_type = db.Column(db.String(50), nullable=False)  # banner, interstitial, video, etc.
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0.0)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdPerformance {self.ad_name} - {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad_id': self.ad_id,
            'ad_name': self.ad_name,
            'ad_type': self.ad_type,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'revenue': self.revenue,
            'ctr': round((self.clicks / self.impressions * 100) if self.impressions > 0 else 0, 2),
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

