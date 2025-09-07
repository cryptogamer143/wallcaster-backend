from datetime import datetime
from .user import db

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpaper.id'), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.String(100), nullable=False)  # copyright, inappropriate, spam, etc.
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, resolved, dismissed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    wallpaper = db.relationship('Wallpaper', backref=db.backref('reports', lazy=True))
    reporter = db.relationship('User', foreign_keys=[reporter_id], backref=db.backref('submitted_reports', lazy=True))
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref=db.backref('reviewed_reports', lazy=True))
    
    def __repr__(self):
        return f'<Report {self.id} - {self.reason}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'wallpaper_id': self.wallpaper_id,
            'wallpaper_title': self.wallpaper.title if self.wallpaper else None,
            'reporter_id': self.reporter_id,
            'reporter_username': self.reporter.username if self.reporter else None,
            'reason': self.reason,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'reviewed_by': self.reviewed_by,
            'reviewer_username': self.reviewer.username if self.reviewer else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

