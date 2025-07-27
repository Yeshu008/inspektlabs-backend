from app import db
from datetime import datetime,timezone

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    inspected_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    damage_report = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'reviewed', 'completed', name='status_enum'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
