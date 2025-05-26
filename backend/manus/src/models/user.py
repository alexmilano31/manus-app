from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(255), nullable=True)
    recovery_codes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation avec les clés API
    api_keys = db.relationship('ApiKey', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'two_factor_enabled': self.two_factor_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def set_recovery_codes(self, codes):
        self.recovery_codes = json.dumps(codes)
    
    def get_recovery_codes(self):
        if self.recovery_codes:
            return json.loads(self.recovery_codes)
        return []


class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # 'binance', 'bitget', etc.
    api_key = db.Column(db.String(255), nullable=False)  # Clé API chiffrée
    api_secret = db.Column(db.String(255), nullable=False)  # Secret API chiffré
    passphrase = db.Column(db.String(255), nullable=True)  # Passphrase chiffrée (si nécessaire)
    label = db.Column(db.String(100), nullable=True)  # Étiquette personnalisée
    permissions = db.Column(db.String(255), nullable=True)  # Permissions accordées à cette clé
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ApiKey {self.platform} - {self.label}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'label': self.label,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
