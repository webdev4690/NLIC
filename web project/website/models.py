from . import db
from datetime import datetime
from flask_login import UserMixin

class AssetRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(100), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float)
    approver = db.Column(db.String(120), nullable=False)
    old_condition = db.Column(db.String(100))
    old_location = db.Column(db.String(100))
    attachment = db.Column(db.String(200))
    old_code = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False)
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)

class ExpenseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(100), nullable=False)      
    item = db.Column(db.String(100), nullable=False)        
    description = db.Column(db.Text, nullable=False)      
    amount = db.Column(db.Float, nullable=False)                  
    expense_month = db.Column(db.String(10), nullable=True)        
    letter_filename = db.Column(db.String(200), nullable=False)    
    approver = db.Column(db.String(120), nullable=False)           
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class DailyLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(100), nullable=False) 
    issue_type = db.Column(db.String(100), nullable=False)
    issue_description = db.Column(db.String(100), nullable=False)
    asset_code = db.Column(db.String(100), nullable=True)
    communication_channel = db.Column(db.String(100), nullable=False)
    issue_generated_by = db.Column(db.String(100), nullable=False)
    replaced_description = db.Column(db.String(100), nullable=True)
    replaced_cost = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    support_station= db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(100), nullable=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False) 
