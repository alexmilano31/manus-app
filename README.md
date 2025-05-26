# Manus - Application Web de Gestion de Portefeuille et d'Analyse de Marché

## 🚀 Présentation

Manus est une application web interactive, moderne et sécurisée conçue pour être le centre de commande unique de l'investisseur moderne. Elle offre une visibilité complète sur les portefeuilles crypto et actions, des outils d'analyse de marché avancés, et une intégration fluide avec les systèmes de trading automatisés (bots).

## 🎯 Objectifs

- Simplifier la gestion multi-plateforme des investissements
- Optimiser la prise de décision grâce à des données enrichies et des alertes intelligentes
- Fournir une expérience utilisateur exceptionnelle sur tous les appareils

## 📈 Fonctionnalités principales

- **Consolidation Financière** : Agrégation de tous les actifs (crypto et actions) en un seul lieu
- **Performance Suivie** : Analyse de la performance historique et en temps réel du portefeuille
- **Détection d'Opportunités** : Alertes proactives sur des opportunités de marché
- **Audit de Trading Bot** : Visualisation et compréhension de l'historique des opérations des bots
- **Information Stratégique** : Suivi des événements économiques majeurs impactant les marchés

## 🧩 Stack Technique

### Frontend
- React (v18+) avec TypeScript
- Tailwind CSS pour le styling
- Recharts/Chart.js pour les graphiques interactifs
- React Query pour la gestion des données asynchrones
- React Router DOM pour le routage

### Backend
- Flask (Python) avec SQLAlchemy
- Base de données MySQL
- JWT pour l'authentification
- Bcrypt pour le hachage des mots de passe

### Déploiement
- Render pour l'hébergement de l'application
- GitHub Actions pour CI/CD

## 🔐 Sécurité

- Authentification à deux facteurs (2FA)
- Gestion sécurisée des clés API
- Sessions sécurisées avec JWT
- Chiffrement des données sensibles

## 📱 Compatibilité

- Design responsive pour tous les appareils
- Optimisation tactile pour les appareils mobiles
- Progressive Web App (PWA) pour une expérience quasi-native

## 🚀 Installation et démarrage

### Prérequis
- Node.js (v18+)
- Python (v3.8+)
- MySQL

### Installation du Frontend
```bash
cd frontend
npm install
npm start
```

### Installation du Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).
