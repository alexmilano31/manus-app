# Guide d'utilisation de Manus

## Introduction

Manus est une application web interactive conçue pour être le centre de commande unique de l'investisseur moderne. Elle offre une visibilité complète sur les portefeuilles crypto et actions, des outils d'analyse de marché avancés, et une intégration fluide avec les systèmes de trading automatisés (bots).

Ce guide vous aidera à prendre en main l'application et à exploiter toutes ses fonctionnalités.

## Table des matières

1. [Accès à l'application](#accès-à-lapplication)
2. [Création de compte et connexion](#création-de-compte-et-connexion)
3. [Configuration de l'authentification à deux facteurs](#configuration-de-lauthentification-à-deux-facteurs)
4. [Ajout de clés API](#ajout-de-clés-api)
5. [Utilisation du tableau de bord](#utilisation-du-tableau-de-bord)
6. [Scanner de marché](#scanner-de-marché)
7. [Suivi des bots de trading](#suivi-des-bots-de-trading)
8. [Calendrier économique](#calendrier-économique)
9. [Paramètres du compte](#paramètres-du-compte)
10. [Assistance et support](#assistance-et-support)

## Accès à l'application

L'application Manus est accessible à l'adresse suivante : [https://manus-app.onrender.com](https://manus-app.onrender.com)

L'application est optimisée pour les navigateurs modernes (Chrome, Firefox, Safari, Edge) et s'adapte parfaitement aux appareils mobiles.

## Création de compte et connexion

### Création d'un compte

1. Accédez à la page d'accueil de Manus
2. Cliquez sur "S'inscrire"
3. Remplissez le formulaire avec vos informations :
   - Nom d'utilisateur (unique)
   - Adresse e-mail
   - Mot de passe (minimum 12 caractères, incluant majuscules, minuscules, chiffres et caractères spéciaux)
4. Validez votre inscription

### Connexion

1. Accédez à la page d'accueil de Manus
2. Cliquez sur "Se connecter"
3. Entrez votre nom d'utilisateur et votre mot de passe
4. Si l'authentification à deux facteurs est activée, vous serez invité à entrer un code

## Configuration de l'authentification à deux facteurs

Pour renforcer la sécurité de votre compte, nous vous recommandons fortement d'activer l'authentification à deux facteurs (2FA).

### Activation du 2FA

1. Connectez-vous à votre compte
2. Accédez à la section "Paramètres" > "Sécurité"
3. Cliquez sur "Activer l'authentification à deux facteurs"
4. Scannez le QR code avec une application d'authentification (Google Authenticator, Authy, etc.)
5. Entrez le code généré par l'application pour confirmer l'activation
6. Conservez précieusement les codes de récupération qui vous sont fournis

### Utilisation des codes de récupération

Si vous perdez accès à votre application d'authentification, vous pouvez utiliser l'un des codes de récupération pour vous connecter. Chaque code ne peut être utilisé qu'une seule fois.

## Ajout de clés API

Pour permettre à Manus d'accéder à vos données de trading, vous devez ajouter les clés API de vos plateformes d'échange.

### Création d'une clé API sur votre plateforme

1. Connectez-vous à votre compte sur la plateforme d'échange (Binance, Bitget, etc.)
2. Accédez à la section de gestion des clés API
3. Créez une nouvelle clé API avec les permissions suivantes :
   - Lecture des soldes et positions
   - Lecture de l'historique des transactions
   - (Optionnel) Permissions de trading si vous souhaitez passer des ordres via Manus

### Ajout de la clé API dans Manus

1. Connectez-vous à votre compte Manus
2. Accédez à la section "Paramètres" > "Connexions API"
3. Cliquez sur "Ajouter une connexion"
4. Sélectionnez la plateforme d'échange
5. Entrez votre clé API, votre clé secrète et éventuellement la passphrase
6. Donnez un nom à cette connexion (ex: "Binance Principal")
7. Validez l'ajout

## Utilisation du tableau de bord

Le tableau de bord est la page principale de Manus, offrant une vue d'ensemble de votre portefeuille.

### Éléments du tableau de bord

- **Résumé du portefeuille** : Valeur totale et variations sur différentes périodes
- **Répartition des actifs** : Graphique montrant la distribution de vos investissements
- **Évolution du portefeuille** : Graphique historique de la valeur de votre portefeuille
- **Détail des actifs** : Tableau listant tous vos actifs avec leurs performances

### Personnalisation du tableau de bord

Vous pouvez personnaliser l'affichage du tableau de bord en :
- Sélectionnant différentes périodes pour les graphiques (24h, 7j, 30j, 1a, Tout)
- Filtrant les actifs par plateforme ou par type
- Triant le tableau des actifs selon différents critères

## Scanner de marché

Le scanner de marché vous permet d'identifier des opportunités d'investissement selon différents critères.

### Types de scanners disponibles

- **RSI** : Détecte les actifs en situation de surachat ou survente
- **Funding Rates** : Identifie les opportunités d'arbitrage sur les marchés à terme
- **Volume** : Repère les actifs avec des volumes de transaction anormalement élevés

### Utilisation du scanner

1. Accédez à la section "Scanner de marché"
2. Sélectionnez le type de scanner souhaité
3. Consultez les résultats dans le tableau
4. Cliquez sur un actif pour accéder à plus de détails

## Suivi des bots de trading

Cette section vous permet de suivre les performances de vos bots de trading automatisés.

### Fonctionnalités disponibles

- **Ordres des bots** : Visualisez tous les ordres passés par vos bots
- **Performance des bots** : Analysez les performances de chaque bot (taux de réussite, PnL)
- **Logs des bots** : Consultez les journaux d'activité pour le débogage

### Filtrage des données

Vous pouvez filtrer les données par :
- Bot spécifique
- Statut des ordres (ouvert, fermé, annulé)
- Période (7j, 30j, 90j, 1a, tout)

## Calendrier économique

Le calendrier économique vous informe des événements majeurs pouvant impacter les marchés financiers.

### Utilisation du calendrier

1. Accédez à la section "Calendrier économique"
2. Consultez les événements à venir
3. Filtrez par importance, pays ou type d'événement
4. Configurez des alertes pour les événements importants

## Paramètres du compte

La section Paramètres vous permet de gérer votre compte et vos préférences.

### Options disponibles

- **Profil** : Modification des informations personnelles
- **Sécurité** : Gestion du mot de passe et de l'authentification à deux facteurs
- **Connexions API** : Gestion des clés API des plateformes d'échange
- **Notifications** : Configuration des alertes et notifications
- **Préférences** : Personnalisation de l'interface (thème, devise de référence)

## Assistance et support

En cas de besoin d'aide ou de problème technique :

- Consultez la documentation en ligne
- Contactez le support à l'adresse support@manus-app.com
- Signalez un bug via le formulaire dédié dans l'application

---

© 2025 Manus - Application de Gestion de Portefeuille
