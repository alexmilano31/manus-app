from flask import Blueprint, request, jsonify
import bcrypt
import pyotp
import secrets
from flask_jwt_extended import create_access_token, create_refresh_token
from src.models.user import db, User
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation des données
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    # Vérification si l'utilisateur existe déjà
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nom d\'utilisateur déjà utilisé'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409
    
    # Validation du mot de passe (min. 12 caractères, majuscules, minuscules, chiffres, caractères spéciaux)
    password = data['password']
    if (len(password) < 12 or not any(c.isupper() for c in password) 
            or not any(c.islower() for c in password) 
            or not any(c.isdigit() for c in password) 
            or not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for c in password)):
        return jsonify({'error': 'Le mot de passe doit contenir au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial'}), 400
    
    # Hashage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Création de l'utilisateur
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Utilisateur créé avec succès', 'user_id': new_user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    # Recherche de l'utilisateur
    user = User.query.filter_by(username=data['username']).first()
    
    # Vérification du mot de passe
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Identifiants invalides'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Compte désactivé'}), 403
    
    # Vérification 2FA si activé
    if user.two_factor_enabled:
        return jsonify({
            'message': 'Authentification à deux facteurs requise',
            'require_2fa': True,
            'user_id': user.id
        }), 200
    
    # Génération des tokens
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Connexion réussie',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('code'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Vérification du code 2FA
    totp = pyotp.TOTP(user.two_factor_secret)
    if not totp.verify(data['code']):
        # Vérification des codes de récupération
        recovery_codes = user.get_recovery_codes()
        if data['code'] in recovery_codes:
            # Supprimer le code de récupération utilisé
            recovery_codes.remove(data['code'])
            user.set_recovery_codes(recovery_codes)
            db.session.commit()
        else:
            return jsonify({'error': 'Code invalide'}), 401
    
    # Génération des tokens
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Authentification réussie',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/setup-2fa', methods=['POST'])
def setup_2fa():
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Génération du secret 2FA
    secret = pyotp.random_base32()
    user.two_factor_secret = secret
    
    # Génération des codes de récupération
    recovery_codes = [secrets.token_hex(5) for _ in range(10)]
    user.set_recovery_codes(recovery_codes)
    
    db.session.commit()
    
    # Création de l'URI pour le QR code
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.email, issuer_name="Manus")
    
    return jsonify({
        'secret': secret,
        'uri': uri,
        'recovery_codes': recovery_codes
    }), 200

@auth_bp.route('/enable-2fa', methods=['POST'])
def enable_2fa():
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('code'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    user = User.query.get(data['user_id'])
    if not user or not user.two_factor_secret:
        return jsonify({'error': 'Configuration 2FA non trouvée'}), 404
    
    # Vérification du code 2FA
    totp = pyotp.TOTP(user.two_factor_secret)
    if not totp.verify(data['code']):
        return jsonify({'error': 'Code invalide'}), 401
    
    # Activation du 2FA
    user.two_factor_enabled = True
    db.session.commit()
    
    return jsonify({'message': 'Authentification à deux facteurs activée'}), 200

@auth_bp.route('/disable-2fa', methods=['POST'])
def disable_2fa():
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('code'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Vérification du code 2FA
    totp = pyotp.TOTP(user.two_factor_secret)
    if not totp.verify(data['code']):
        return jsonify({'error': 'Code invalide'}), 401
    
    # Désactivation du 2FA
    user.two_factor_enabled = False
    user.two_factor_secret = None
    user.recovery_codes = None
    db.session.commit()
    
    return jsonify({'message': 'Authentification à deux facteurs désactivée'}), 200
