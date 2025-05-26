# Guide de déploiement SQLite - Manus

Ce guide explique comment déployer l'application Manus avec SQLite comme base de données.

## Prérequis

- Python 3.8 ou supérieur
- Node.js 14 ou supérieur
- Git (optionnel)

## Étape 1 : Préparation du backend

1. Naviguez vers le dossier du backend :
   ```bash
   cd manus-project/backend/manus
   ```

2. Créez un environnement virtuel Python :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Vérifiez que la configuration SQLite est bien en place dans `src/main.py` :
   ```python
   # Configuration de la base de données SQLite
   db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'manus.db')
   app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
   ```

## Étape 2 : Démarrage du backend

1. Lancez l'application Flask :
   ```bash
   python src/main.py
   ```

2. Le serveur backend devrait démarrer sur http://localhost:5000

## Étape 3 : Configuration du frontend pour pointer vers le backend local

Si vous utilisez le frontend déployé (https://armciunm.manus.space), vous devrez configurer CORS sur votre backend pour accepter les requêtes depuis ce domaine.

Pour utiliser le frontend en local :

1. Naviguez vers le dossier du frontend :
   ```bash
   cd manus-project/frontend
   ```

2. Installez les dépendances :
   ```bash
   npm install
   ```

3. Modifiez le fichier `.env` ou créez-le s'il n'existe pas :
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

4. Lancez le serveur de développement :
   ```bash
   npm start
   ```

5. Le frontend devrait démarrer sur http://localhost:3000

## Déploiement sur Render

Pour déployer sur Render avec SQLite :

1. Créez un nouveau Web Service sur Render
2. Connectez votre dépôt GitHub
3. Configurez le service :
   - **Build Command** : `pip install -r backend/manus/requirements.txt`
   - **Start Command** : `cd backend/manus && python src/main.py`
   - **Environment Variables** :
     - `SECRET_KEY` : Une clé secrète pour JWT
     - `ENCRYPTION_KEY` : Une clé pour le chiffrement des clés API (32 caractères)

4. Déployez le service

## Avantages de SQLite

- Pas besoin de configurer un serveur de base de données séparé
- Fichier unique facile à sauvegarder
- Parfait pour les démos et les tests
- Fonctionne sur pratiquement tous les environnements

## Limitations de SQLite

- Moins performant pour les applications à forte charge
- Pas adapté pour les accès concurrents intensifs
- Limité en termes de fonctionnalités avancées par rapport à MySQL/PostgreSQL

## Migration future

Si vous souhaitez migrer vers MySQL ou PostgreSQL à l'avenir, il vous suffira de modifier la chaîne de connexion dans `src/main.py` et d'installer les dépendances appropriées.
