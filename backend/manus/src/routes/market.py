from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, ApiKey
import requests
from datetime import datetime, timedelta
import json
import os
from cryptography.fernet import Fernet

market_bp = Blueprint('market', __name__)

# Clé de chiffrement pour les clés API (en production, utiliser une variable d'environnement)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'votre_clé_de_chiffrement_à_remplacer_en_production')
cipher_suite = Fernet(ENCRYPTION_KEY.encode() if len(ENCRYPTION_KEY) == 32 else Fernet.generate_key())

@market_bp.route('/opportunities', methods=['GET'])
@jwt_required()
def get_opportunities():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Récupération des paramètres de filtrage
    scanner_type = request.args.get('type', 'all')  # 'rsi', 'funding', 'volume', 'all'
    
    # Récupération des clés API de l'utilisateur
    api_keys = ApiKey.query.filter_by(user_id=user_id, is_active=True).all()
    
    if not api_keys:
        return jsonify({'error': 'Aucune clé API configurée'}), 400
    
    # Initialisation des résultats
    opportunities = []
    
    # Pour chaque clé API, rechercher des opportunités
    for api_key in api_keys:
        try:
            # Déchiffrement des clés
            decrypted_api_key = cipher_suite.decrypt(api_key.api_key.encode()).decode()
            decrypted_api_secret = cipher_suite.decrypt(api_key.api_secret.encode()).decode()
            
            # Logique selon la plateforme
            if api_key.platform == 'binance':
                # Récupération des données de marché
                if scanner_type in ['rsi', 'all']:
                    # Exemple: Recherche de cryptos avec RSI extrême
                    # En production, utiliser une bibliothèque comme python-binance et calculer le RSI
                    # Simulation de données pour démonstration
                    rsi_opportunities = [
                        {
                            'symbol': 'BTC/USDT',
                            'name': 'Bitcoin',
                            'current_price': 45000,
                            'rsi_1h': 28,
                            'rsi_4h': 32,
                            'rsi_1d': 42,
                            'condition': 'RSI survendu',
                            'timeframe': '1h',
                            'platform': api_key.platform
                        },
                        {
                            'symbol': 'ETH/USDT',
                            'name': 'Ethereum',
                            'current_price': 3200,
                            'rsi_1h': 72,
                            'rsi_4h': 68,
                            'rsi_1d': 58,
                            'condition': 'RSI suracheté',
                            'timeframe': '1h',
                            'platform': api_key.platform
                        }
                    ]
                    opportunities.extend(rsi_opportunities)
                
                if scanner_type in ['funding', 'all']:
                    # Exemple: Recherche de funding rates anormaux
                    # En production, utiliser l'API Binance Futures
                    # Simulation de données pour démonstration
                    funding_opportunities = [
                        {
                            'symbol': 'BTC/USDT',
                            'name': 'Bitcoin',
                            'current_price': 45000,
                            'funding_rate': -0.06,
                            'next_funding_time': (datetime.now() + timedelta(hours=2)).isoformat(),
                            'condition': 'Funding rate négatif élevé',
                            'platform': api_key.platform
                        },
                        {
                            'symbol': 'SOL/USDT',
                            'name': 'Solana',
                            'current_price': 120,
                            'funding_rate': 0.08,
                            'next_funding_time': (datetime.now() + timedelta(hours=2)).isoformat(),
                            'condition': 'Funding rate positif élevé',
                            'platform': api_key.platform
                        }
                    ]
                    opportunities.extend(funding_opportunities)
                
                if scanner_type in ['volume', 'all']:
                    # Exemple: Recherche de volumes anormaux
                    # En production, utiliser l'API Binance
                    # Simulation de données pour démonstration
                    volume_opportunities = [
                        {
                            'symbol': 'DOGE/USDT',
                            'name': 'Dogecoin',
                            'current_price': 0.12,
                            'volume_24h': 1200000000,
                            'volume_change': 320,
                            'condition': 'Volume en forte hausse',
                            'platform': api_key.platform
                        }
                    ]
                    opportunities.extend(volume_opportunities)
            
            # Autres plateformes...
            
        except Exception as e:
            # Log l'erreur mais continuer avec les autres clés API
            print(f"Erreur lors de la recherche d'opportunités pour {api_key.platform}: {str(e)}")
    
    return jsonify({
        'opportunities': opportunities
    }), 200

@market_bp.route('/economic-calendar', methods=['GET'])
@jwt_required()
def get_economic_calendar():
    # Paramètres de filtrage
    start_date = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
    importance = request.args.get('importance', 'all')  # 'low', 'medium', 'high', 'all'
    countries = request.args.get('countries', 'all')  # 'US,EU,JP' ou 'all'
    
    # En production, utiliser une API comme Investing.com ou Forex Factory
    # Simulation de données pour démonstration
    events = [
        {
            'id': 1,
            'title': 'Publication du taux de chômage US',
            'country': 'US',
            'date': (datetime.now() + timedelta(days=2)).isoformat(),
            'time': '12:30:00',
            'importance': 'high',
            'previous': '3.8%',
            'forecast': '3.7%',
            'actual': None
        },
        {
            'id': 2,
            'title': 'Décision de taux BCE',
            'country': 'EU',
            'date': (datetime.now() + timedelta(days=3)).isoformat(),
            'time': '13:45:00',
            'importance': 'high',
            'previous': '4.25%',
            'forecast': '4.25%',
            'actual': None
        },
        {
            'id': 3,
            'title': 'PIB Japon T1',
            'country': 'JP',
            'date': (datetime.now() + timedelta(days=5)).isoformat(),
            'time': '00:50:00',
            'importance': 'medium',
            'previous': '0.1%',
            'forecast': '0.2%',
            'actual': None
        }
    ]
    
    # Filtrage par importance
    if importance != 'all':
        events = [event for event in events if event['importance'] == importance]
    
    # Filtrage par pays
    if countries != 'all':
        country_list = countries.split(',')
        events = [event for event in events if event['country'] in country_list]
    
    return jsonify({
        'events': events
    }), 200
