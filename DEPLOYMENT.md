# 🛡️ CyberCoach - Guide de Déploiement

## 📋 Prérequis

- Python 3.9+ 
- Un compte Groq (gratuit): https://console.groq.com
- Un compte Streamlit Cloud (gratuit): https://streamlit.io/cloud
- Un compte GitHub

## 🚀 Installation Locale - Démarrage Rapide

### Option 1: Windows (Simple) 🎯

Cliquez simplement sur **`run.bat`** dans le dossier du projet!

Ce script installera automatiquement les dépendances et lancera Streamlit.

### Option 2: Installation Manuelle

#### 1. Ouvrir PowerShell ou Command Prompt dans le dossier

```bash
cd d:\new projet\cybercoach
```

#### 2. Installer les dépendances directement (pas de venv nécessaire)

```bash
pip install streamlit==1.32.0 groq==0.7.0 pandas==2.1.3 plotly==5.18.0 python-dotenv==1.0.0
```

#### 3. Configurer les variables d'environnement

Créez un fichier `.env` à partir de `.env.example` et ajoutez votre clé Groq (ne la partagez pas):

```bash
cp .env.example .env
# Éditez .env et ajoutez votre clé GROQ_API_KEY
```

#### 4. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre à `http://localhost:8501`

## 🌐 Déploiement sur Streamlit Cloud ou Docker

### Option A: Streamlit Cloud (rapide)

Assurez-vous que votre projet est sur GitHub et suivez les étapes standards de Streamlit Cloud.

### Option B: Déploiement via Docker (recommandé pour production / local)

1. Construisez et démarrez les services (Streamlit + FastAPI phishing tracker):

```bash
# Depuis la racine du projet
docker compose up --build
```

2. Services exposés:
- Streamlit app: http://localhost:8501
- Phishing tracker API: http://localhost:8000

Note: The phishing tracker exposes a public redirect endpoint for tracking links: `GET /r/{campaign_id}?email=...` which records a click and returns a brief confirmation JSON. Use the generated tracking URL in simulation emails.
3. Ajoutez la variable d'environnement `CYBERCOACH_DB_URL` si vous souhaitez pointer vers une DB externe.

### Configurer les secrets

- En local, utilisez `.env` et exportez `GROQ_API_KEY`
- En production (Docker), utilisez les secrets de votre orchestrateur (Docker secrets, Kubernetes Secrets, etc.)

### Remarques

- Le microservice `phishing_service` écoute par défaut sur le port 8000 et stocke les événements dans `./cybercoach.db` (SQLite).
- Pour la production, remplacez SQLite par Postgres et ajustez `CYBERCOACH_DB_URL`.

## 📁 Structure du Projet

```
cybercoach/
├── app.py                # Application principale
├── chatbot.py            # Module Chatbot (FREE)
├── quiz.py               # Module Quiz & Tracking (STANDARD)
├── config.py             # Configuration globale
├── requirements.txt      # Dépendances Python
├── .env.example          # Exemple de variables d'env
├── .streamlit/
│   └── config.toml       # Configuration Streamlit
└── README.md             # Ce fichier
```

## 🔧 Développement Futur

### Module PREMIUM (Phishing Simulation)

La structure pour le module PREMIUM existe déjà. Pour l'ajouter:

1. Créer `phishing.py` avec la logique de simulation
2. Créer un microservice de tracking léger (FastAPI ou Flask)
3. Ajouter l'onglet PREMIUM à `app.py`

### Variables Session à Utiliser

L'app utilise `st.session_state` pour:
- Historique de chat
- Données utilisateur
- Progrès des quiz
- Scores

## 📊 Fonctionnalités Actuelles

### ✅ MVP FREE - Chatbot
- Chatbot IA avec Groq API
- Historique de conversation
- Réponses pédagogiques en cybersécurité

### ✅ STANDARD - Quiz & Tracking
- 4 quiz intégrés (Phishing, Mots de passe, Ransomware, Télétravail)
- Identification utilisateur
- Suivi des scores
- Progrès par département
- Corrections détaillées

### 🔜 PREMIUM - Phishing Simulation
- Campagnes de phishing simulées
- Tracking des clics/soumissions
- Tableau de bord exécutif
- Calcul du TRV (Taux de Risque)

## 🐛 Dépannage

### "GROQ_API_KEY non trouvée"
- Vérifier que le fichier `.env` existe
- Vérifier que la clé est bien copiée de https://console.groq.com

### L'app charge lentement
- Les réponses du chatbot peuvent prendre 2-3 secondes
- C'est normal pour la première requête

### Erreur de connexion Groq
- Vérifier votre connexion internet
- Vérifier que votre API key est valide
- Vérifier les quotas Groq (gratuit = limité)

## 📞 Support

- Email: support@cybercoach.fr
- Slack: [À ajouter]
- Docs: [À ajouter]

---

**Version**: 1.0 MVP  
**Date**: Décembre 2024  
**Status**: En développement
