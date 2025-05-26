# Documentation Technique - Manus

## Architecture Globale

Manus est une application web moderne basée sur une architecture client-serveur :

- **Frontend** : Application React avec TypeScript et Tailwind CSS
- **Backend** : API REST Flask avec MySQL comme base de données
- **Déploiement** : Hébergement sur Render avec CI/CD via GitHub Actions

## Structure du Projet

```
manus-project/
├── frontend/                # Application React/TypeScript
│   ├── src/
│   │   ├── components/      # Composants réutilisables
│   │   ├── pages/           # Pages de l'application
│   │   ├── services/        # Services d'API et utilitaires
│   │   ├── hooks/           # Hooks React personnalisés
│   │   ├── utils/           # Fonctions utilitaires
│   │   ├── assets/          # Ressources statiques
│   │   └── types/           # Définitions TypeScript
│   └── public/              # Fichiers statiques publics
│
├── backend/
│   └── manus/
│       ├── src/
│       │   ├── models/      # Modèles de données SQLAlchemy
│       │   ├── routes/      # Routes API Flask
│       │   ├── static/      # Fichiers statiques (build frontend)
│       │   └── main.py      # Point d'entrée de l'application
│       ├── tests/           # Tests unitaires et d'intégration
│       └── requirements.txt # Dépendances Python
│
├── docs/                    # Documentation
│   ├── user_guide.md        # Guide utilisateur
│   └── technical_docs.md    # Documentation technique
│
├── .github/
│   └── workflows/           # Configuration CI/CD
│       └── ci-cd.yml        # Pipeline GitHub Actions
│
├── .gitignore               # Fichiers ignorés par Git
└── README.md                # Présentation du projet
```

## Stack Technique

### Frontend

- **Framework** : React 18+
- **Langage** : TypeScript
- **Styling** : Tailwind CSS
- **Gestion d'état** : React Query pour les données asynchrones
- **Routage** : React Router DOM
- **Graphiques** : Recharts
- **Requêtes API** : Axios

### Backend

- **Framework** : Flask (Python)
- **ORM** : SQLAlchemy
- **Base de données** : MySQL
- **Authentification** : JWT (Flask-JWT-Extended)
- **Sécurité** : Bcrypt pour le hachage des mots de passe, CORS
- **2FA** : PyOTP pour l'authentification à deux facteurs

### Déploiement

- **Hébergement** : Render
- **CI/CD** : GitHub Actions
- **Conteneurisation** : Docker (via Render)

## Modèles de Données

### User

Représente un utilisateur de l'application.

```python
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
```

### ApiKey

Stocke les clés API des plateformes d'échange.

```python
class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    api_secret = db.Column(db.String(255), nullable=False)
    passphrase = db.Column(db.String(255), nullable=True)
    label = db.Column(db.String(100), nullable=True)
    permissions = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## API Endpoints

### Authentification

- `POST /api/auth/register` : Inscription d'un nouvel utilisateur
- `POST /api/auth/login` : Connexion utilisateur
- `POST /api/auth/verify-2fa` : Vérification du code 2FA
- `POST /api/auth/setup-2fa` : Configuration du 2FA
- `POST /api/auth/enable-2fa` : Activation du 2FA
- `POST /api/auth/disable-2fa` : Désactivation du 2FA

### Gestion du Portefeuille

- `GET /api/portfolio/api-keys` : Liste des clés API
- `POST /api/portfolio/api-keys` : Ajout d'une clé API
- `DELETE /api/portfolio/api-keys/<key_id>` : Suppression d'une clé API
- `GET /api/portfolio/balance` : Solde consolidé du portefeuille
- `GET /api/portfolio/transactions` : Historique des transactions

### Scanner de Marché

- `GET /api/market/opportunities` : Opportunités de marché
- `GET /api/market/economic-calendar` : Calendrier économique

### Suivi des Bots

- `GET /api/bots/orders` : Ordres des bots de trading
- `GET /api/bots/performance` : Performance des bots
- `GET /api/bots/logs` : Logs des bots

## Sécurité

### Authentification et Autorisation

- Utilisation de JWT (JSON Web Tokens) pour l'authentification stateless
- Tokens d'accès à courte durée de vie (1 heure)
- Tokens de rafraîchissement pour renouveler l'accès
- Middleware JWT pour protéger les routes sensibles

### Protection des Données Sensibles

- Hachage des mots de passe avec Bcrypt
- Chiffrement des clés API avec Fernet (AES-128)
- Authentification à deux facteurs (2FA) basée sur TOTP
- Codes de récupération pour l'accès d'urgence

### Validation des Entrées

- Validation stricte des données utilisateur
- Protection contre les injections SQL via ORM
- Validation des clés API avant stockage

## Tests

### Tests Unitaires

- Tests des modèles de données
- Tests des fonctions utilitaires
- Tests des services

### Tests d'Intégration

- Tests des routes API
- Tests de l'authentification
- Tests des interactions avec la base de données

## Déploiement

### Pipeline CI/CD

Le pipeline CI/CD est configuré via GitHub Actions et comprend :

1. **Test du Backend** :
   - Exécution des tests unitaires et d'intégration
   - Vérification de la couverture de code

2. **Test du Frontend** :
   - Exécution des tests unitaires
   - Build de production

3. **Déploiement** :
   - Build du frontend
   - Copie des fichiers statiques dans le dossier backend
   - Déploiement sur Render via webhook

### Configuration Render

- **Type de service** : Web Service
- **Runtime** : Python
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python src/main.py`
- **Variables d'environnement** :
  - `DB_USERNAME` : Nom d'utilisateur MySQL
  - `DB_PASSWORD` : Mot de passe MySQL
  - `DB_HOST` : Hôte MySQL
  - `DB_PORT` : Port MySQL
  - `DB_NAME` : Nom de la base de données
  - `SECRET_KEY` : Clé secrète pour JWT
  - `ENCRYPTION_KEY` : Clé pour le chiffrement des clés API

## Maintenance et Évolution

### Monitoring

- Logs d'application via Render
- Surveillance des performances et des erreurs

### Sauvegarde

- Sauvegarde automatique de la base de données MySQL

### Futures Améliorations

- Intégration de plus de plateformes d'échange
- Amélioration des algorithmes de détection d'opportunités
- Ajout de fonctionnalités de trading direct
- Rapports fiscaux et gestion des taxes
- Support multi-langues et multi-devises

## Ressources

- [Documentation React](https://reactjs.org/docs/getting-started.html)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation Tailwind CSS](https://tailwindcss.com/docs)
- [Documentation Render](https://render.com/docs)
