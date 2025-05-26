from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, ApiKey
import os
from cryptography.fernet import Fernet
import requests
import json
from datetime import datetime

portfolio_bp = Blueprint('portfolio', __name__)

# Clé de chiffrement pour les clés API (en production, utiliser une variable d'environnement)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'votre_clé_de_chiffrement_à_remplacer_en_production')
cipher_suite = Fernet(ENCRYPTION_KEY.encode() if len(ENCRYPTION_KEY) == 32 else Fernet.generate_key())

@portfolio_bp.route('/api-keys', methods=['GET'])
@jwt_required()
def get_api_keys():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    api_keys = ApiKey.query.filter_by(user_id=user_id).all()
    return jsonify({
        'api_keys': [key.to_dict() for key in api_keys]
    }), 200

@portfolio_bp.route('/api-keys', methods=['POST'])
@jwt_required()
def add_api_key():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    
    # Validation des données
    if not data or not data.get('platform') or not data.get('api_key') or not data.get('api_secret'):
        return jsonify({'error': 'Données incomplètes'}), 400
    
    # Chiffrement des clés API
    encrypted_api_key = cipher_suite.encrypt(data['api_key'].encode()).decode()
    encrypted_api_secret = cipher_suite.encrypt(data['api_secret'].encode()).decode()
    
    # Chiffrement de la passphrase si fournie
    encrypted_passphrase = None
    if data.get('passphrase'):
        encrypted_passphrase = cipher_suite.encrypt(data['passphrase'].encode()).decode()
    
    # Création de la clé API
    new_api_key = ApiKey(
        user_id=user_id,
        platform=data['platform'],
        api_key=encrypted_api_key,
        api_secret=encrypted_api_secret,
        passphrase=encrypted_passphrase,
        label=data.get('label', f"{data['platform']} API"),
        permissions=data.get('permissions', 'read')
    )
    
    # Test de connexion à l'API
    try:
        # Déchiffrement pour le test
        api_key = cipher_suite.decrypt(encrypted_api_key.encode()).decode()
        api_secret = cipher_suite.decrypt(encrypted_api_secret.encode()).decode()
        
        # Logique de test selon la plateforme
        if data['platform'] == 'binance':
            # Test de connexion à l'API Binance
            # En production, utiliser une bibliothèque comme python-binance
            response = requests.get(
                'https://api.binance.com/api/v3/account',
                params={'timestamp': int(datetime.now().timestamp() * 1000)},
                headers={'X-MBX-APIKEY': api_key}
                # En production, ajouter la signature HMAC
            )
            if response.status_code != 200:
                return jsonify({'error': 'Échec de la connexion à l\'API Binance'}), 400
        
        elif data['platform'] == 'bitget':
            # Test de connexion à l'API Bitget
            # Logique similaire à Binance
            pass
        
        # Autres plateformes...
        
    except Exception as e:
        return jsonify({'error': f'Échec du test de connexion: {str(e)}'}), 400
    
    db.session.add(new_api_key)
    db.session.commit()
    
    return jsonify({
        'message': 'Clé API ajoutée avec succès',
        'api_key': new_api_key.to_dict()
    }), 201

@portfolio_bp.route('/api-keys/<int:key_id>', methods=['DELETE'])
@jwt_required()
def delete_api_key(key_id):
    user_id = get_jwt_identity()
    
    api_key = ApiKey.query.filter_by(id=key_id, user_id=user_id).first()
    if not api_key:
        return jsonify({'error': 'Clé API non trouvée ou non autorisée'}), 404
    
    db.session.delete(api_key)
    db.session.commit()
    
    return jsonify({'message': 'Clé API supprimée avec succès'}), 200

@portfolio_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Récupération des clés API de l'utilisateur
    api_keys = ApiKey.query.filter_by(user_id=user_id, is_active=True).all()
    
    if not api_keys:
        return jsonify({'error': 'Aucune clé API configurée'}), 400
    
    # Initialisation des résultats
    total_balance = 0
    assets = {}
    balances_by_platform = {}
    
    # Pour chaque clé API, récupérer les soldes
    for api_key in api_keys:
        try:
            # Déchiffrement des clés
            decrypted_api_key = cipher_suite.decrypt(api_key.api_key.encode()).decode()
            decrypted_api_secret = cipher_suite.decrypt(api_key.api_secret.encode()).decode()
            
            platform_balance = 0
            platform_assets = {}
            
            # Logique selon la plateforme
            if api_key.platform == 'binance':
                # En production, utiliser une bibliothèque comme python-binance
                # Exemple simplifié
                response = requests.get(
                    'https://api.binance.com/api/v3/account',
                    params={'timestamp': int(datetime.now().timestamp() * 1000)},
                    headers={'X-MBX-APIKEY': decrypted_api_key}
                    # En production, ajouter la signature HMAC
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for balance in data.get('balances', []):
                        asset = balance['asset']
                        free = float(balance['free'])
                        locked = float(balance['locked'])
                        total = free + locked
                        
                        if total > 0:
                            # Conversion en USD (à implémenter avec des prix réels)
                            usd_value = total * 1  # Placeholder
                            
                            platform_assets[asset] = {
                                'amount': total,
                                'usd_value': usd_value
                            }
                            platform_balance += usd_value
                            
                            # Agrégation globale
                            if asset in assets:
                                assets[asset]['amount'] += total
                                assets[asset]['usd_value'] += usd_value
                            else:
                                assets[asset] = {
                                    'amount': total,
                                    'usd_value': usd_value
                                }
            
            # Autres plateformes...
            
            balances_by_platform[api_key.platform] = {
                'total_usd': platform_balance,
                'assets': platform_assets
            }
            
            total_balance += platform_balance
            
        except Exception as e:
            # Log l'erreur mais continuer avec les autres clés API
            print(f"Erreur lors de la récupération des soldes pour {api_key.platform}: {str(e)}")
    
    return jsonify({
        'total_balance_usd': total_balance,
        'assets': assets,
        'platforms': balances_by_platform
    }), 200

@portfolio_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Paramètres de filtrage
    platform = request.args.get('platform')
    asset = request.args.get('asset')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Récupération des clés API de l'utilisateur
    query = ApiKey.query.filter_by(user_id=user_id, is_active=True)
    if platform:
        query = query.filter_by(platform=platform)
    api_keys = query.all()
    
    if not api_keys:
        return jsonify({'error': 'Aucune clé API configurée'}), 400
    
    # Initialisation des résultats
    transactions = []
    
    # Pour chaque clé API, récupérer les transactions
    for api_key in api_keys:
        try:
            # Déchiffrement des clés
            decrypted_api_key = cipher_suite.decrypt(api_key.api_key.encode()).decode()
            decrypted_api_secret = cipher_suite.decrypt(api_key.api_secret.encode()).decode()
            
            # Logique selon la plateforme
            if api_key.platform == 'binance':
                # En production, utiliser une bibliothèque comme python-binance
                # Exemple simplifié
                params = {'timestamp': int(datetime.now().timestamp() * 1000)}
                
                # Ajout des filtres
                if asset:
                    params['symbol'] = asset
                if start_date:
                    params['startTime'] = int(datetime.fromisoformat(start_date).timestamp() * 1000)
                if end_date:
                    params['endTime'] = int(datetime.fromisoformat(end_date).timestamp() * 1000)
                
                response = requests.get(
                    'https://api.binance.com/api/v3/myTrades',
                    params=params,
                    headers={'X-MBX-APIKEY': decrypted_api_key}
                    # En production, ajouter la signature HMAC
                )
                
                if response.status_code == 200:
                    platform_transactions = response.json()
                    for tx in platform_transactions:
                        transactions.append({
                            'platform': api_key.platform,
                            'id': tx['id'],
                            'symbol': tx['symbol'],
                            'price': float(tx['price']),
                            'quantity': float(tx['qty']),
                            'commission': float(tx['commission']),
                            'commission_asset': tx['commissionAsset'],
                            'time': datetime.fromtimestamp(tx['time'] / 1000).isoformat(),
                            'is_buyer': tx['isBuyer'],
                            'is_maker': tx['isMaker']
                        })
            
            # Autres plateformes...
            
        except Exception as e:
            # Log l'erreur mais continuer avec les autres clés API
            print(f"Erreur lors de la récupération des transactions pour {api_key.platform}: {str(e)}")
    
    # Tri des transactions par date
    transactions.sort(key=lambda x: x['time'], reverse=True)
    
    return jsonify({
        'transactions': transactions
    }), 200
