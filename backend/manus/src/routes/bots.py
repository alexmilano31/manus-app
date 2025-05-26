from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, ApiKey
import requests
from datetime import datetime
import json
import os
from cryptography.fernet import Fernet

bots_bp = Blueprint('bots', __name__)

# Clé de chiffrement pour les clés API (en production, utiliser une variable d'environnement)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'votre_clé_de_chiffrement_à_remplacer_en_production')
cipher_suite = Fernet(ENCRYPTION_KEY.encode() if len(ENCRYPTION_KEY) == 32 else Fernet.generate_key())

@bots_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_bot_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Paramètres de filtrage
    bot_id = request.args.get('bot_id')
    status = request.args.get('status')  # 'open', 'closed', 'canceled', 'error'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # En production, interroger l'API des bots sur Render
    # Simulation de données pour démonstration
    orders = [
        {
            'id': '12345',
            'bot_id': 'btc_grid_bot',
            'bot_name': 'BTC Grid Trading',
            'exchange': 'Binance',
            'symbol': 'BTC/USDT',
            'type': 'limit',
            'side': 'buy',
            'price': 44500,
            'amount': 0.05,
            'status': 'closed',
            'filled': 0.05,
            'remaining': 0,
            'cost': 2225,
            'fee': 1.11,
            'created_at': '2025-05-23T14:30:00Z',
            'updated_at': '2025-05-23T14:30:05Z',
            'closed_at': '2025-05-23T14:30:05Z',
            'pnl': 25.5,
            'pnl_percent': 1.15
        },
        {
            'id': '12346',
            'bot_id': 'btc_grid_bot',
            'bot_name': 'BTC Grid Trading',
            'exchange': 'Binance',
            'symbol': 'BTC/USDT',
            'type': 'limit',
            'side': 'sell',
            'price': 45000,
            'amount': 0.05,
            'status': 'open',
            'filled': 0,
            'remaining': 0.05,
            'cost': 0,
            'fee': 0,
            'created_at': '2025-05-24T08:10:00Z',
            'updated_at': '2025-05-24T08:10:00Z',
            'closed_at': None,
            'pnl': None,
            'pnl_percent': None
        },
        {
            'id': '12347',
            'bot_id': 'eth_dca_bot',
            'bot_name': 'ETH DCA Strategy',
            'exchange': 'Bitget',
            'symbol': 'ETH/USDT',
            'type': 'market',
            'side': 'buy',
            'price': 3150,
            'amount': 0.5,
            'status': 'closed',
            'filled': 0.5,
            'remaining': 0,
            'cost': 1575,
            'fee': 0.79,
            'created_at': '2025-05-22T10:00:00Z',
            'updated_at': '2025-05-22T10:00:02Z',
            'closed_at': '2025-05-22T10:00:02Z',
            'pnl': -15.75,
            'pnl_percent': -1.0
        }
    ]
    
    # Filtrage par bot_id
    if bot_id:
        orders = [order for order in orders if order['bot_id'] == bot_id]
    
    # Filtrage par status
    if status:
        orders = [order for order in orders if order['status'] == status]
    
    # Filtrage par date
    if start_date:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        orders = [order for order in orders if datetime.fromisoformat(order['created_at'].replace('Z', '+00:00')) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        orders = [order for order in orders if datetime.fromisoformat(order['created_at'].replace('Z', '+00:00')) <= end]
    
    return jsonify({
        'orders': orders
    }), 200

@bots_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_bot_performance():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Paramètres de filtrage
    bot_id = request.args.get('bot_id')
    period = request.args.get('period', '30d')  # '7d', '30d', '90d', '1y', 'all'
    
    # En production, interroger l'API des bots sur Render
    # Simulation de données pour démonstration
    bots_performance = [
        {
            'id': 'btc_grid_bot',
            'name': 'BTC Grid Trading',
            'exchange': 'Binance',
            'symbol': 'BTC/USDT',
            'strategy': 'Grid Trading',
            'start_date': '2025-04-01T00:00:00Z',
            'total_trades': 42,
            'win_rate': 68.5,
            'profit_factor': 1.8,
            'total_pnl': 1250.75,
            'total_pnl_percent': 12.5,
            'daily_pnl': [
                {'date': '2025-05-23', 'pnl': 45.5, 'pnl_percent': 0.45},
                {'date': '2025-05-22', 'pnl': -12.3, 'pnl_percent': -0.12},
                {'date': '2025-05-21', 'pnl': 28.7, 'pnl_percent': 0.29}
            ]
        },
        {
            'id': 'eth_dca_bot',
            'name': 'ETH DCA Strategy',
            'exchange': 'Bitget',
            'symbol': 'ETH/USDT',
            'strategy': 'Dollar Cost Averaging',
            'start_date': '2025-03-15T00:00:00Z',
            'total_trades': 10,
            'win_rate': 60.0,
            'profit_factor': 1.5,
            'total_pnl': 320.45,
            'total_pnl_percent': 8.2,
            'daily_pnl': [
                {'date': '2025-05-23', 'pnl': 0, 'pnl_percent': 0},
                {'date': '2025-05-22', 'pnl': -15.75, 'pnl_percent': -0.4},
                {'date': '2025-05-21', 'pnl': 0, 'pnl_percent': 0}
            ]
        }
    ]
    
    # Filtrage par bot_id
    if bot_id:
        bots_performance = [bot for bot in bots_performance if bot['id'] == bot_id]
    
    return jsonify({
        'bots': bots_performance
    }), 200

@bots_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_bot_logs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Paramètres de filtrage
    bot_id = request.args.get('bot_id')
    level = request.args.get('level', 'all')  # 'info', 'warning', 'error', 'all'
    limit = request.args.get('limit', 100, type=int)
    
    if not bot_id:
        return jsonify({'error': 'ID du bot requis'}), 400
    
    # En production, interroger l'API des bots sur Render
    # Simulation de données pour démonstration
    logs = [
        {
            'timestamp': '2025-05-24T08:10:00Z',
            'level': 'info',
            'message': 'Ordre de vente placé: BTC/USDT à 45000 USDT'
        },
        {
            'timestamp': '2025-05-23T14:30:05Z',
            'level': 'info',
            'message': 'Ordre d\'achat exécuté: BTC/USDT à 44500 USDT'
        },
        {
            'timestamp': '2025-05-23T14:29:00Z',
            'level': 'info',
            'message': 'Ordre d\'achat placé: BTC/USDT à 44500 USDT'
        },
        {
            'timestamp': '2025-05-23T12:00:00Z',
            'level': 'warning',
            'message': 'Latence élevée détectée avec l\'API Binance'
        },
        {
            'timestamp': '2025-05-22T18:45:30Z',
            'level': 'error',
            'message': 'Échec de connexion à l\'API Binance, nouvelle tentative dans 60 secondes'
        }
    ]
    
    # Filtrage par level
    if level != 'all':
        logs = [log for log in logs if log['level'] == level]
    
    # Limitation du nombre de logs
    logs = logs[:limit]
    
    return jsonify({
        'logs': logs
    }), 200
