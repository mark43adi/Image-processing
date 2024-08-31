from app import db
from datetime import datetime

class ProcessingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(36), unique=True, index=True)
    status = db.Column(db.String(20))  # 'pending', 'processing', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(36), db.ForeignKey('processing_request.request_id'), index=True)
    serial_number = db.Column(db.Integer, index=True)  
    name = db.Column(db.String(100))
    input_image_urls = db.Column(db.Text)  
    output_image_urls = db.Column(db.Text)  

    