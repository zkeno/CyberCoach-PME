# CyberCoach

🛡️ **Assistant IA de Cybersécurité pour PME**

CyberCoach est une plateforme intelligente qui transforme vos collaborateurs en première ligne de défense contre les cybermenaces.

## ✨ Fonctionnalités

### 🆓 Offre FREE - Chatbot
- Accès illimité à CyberCoach Chatbot
- Questions sur la cybersécurité 24/7
- Réponses pédagogiques et bienveillantes
- Powered by Groq Llama 3

### 💳 Offre STANDARD - Quiz & Formation
- Quiz interactifs (4 modules inclus)
- Suivi des progrès par collaborateur
- Taux de complétion & Scores moyens par département
- Rapports de conformité
- Preuve de formation pour auditeurs

### 🚀 Offre PREMIUM - Gestion du Risque (À venir)
- Simulations de phishing réelles
- Tableau de Bord Exécutif (TRV)
- Mesure de résistance réelle aux cybermenaces
- Remédiation automatique

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.9+
- Une clé API Groq (gratuite): https://console.groq.com

### Installation

```bash
# Cloner le projet
git clone https://github.com/yourusername/cybercoach.git
cd cybercoach

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre clé Groq
```

### Lancer l'application

```bash
streamlit run app.py
```

Ouvrir `http://localhost:8501`

<!-- ci: trigger run -->
## 📁 Structure du Projet

```
cybercoach/
├── app.py              # Application principale Streamlit
├── chatbot.py          # Module Chatbot
├── quiz.py             # Module Quiz & Tracking
├── config.py           # Configuration et données
├── requirements.txt    # Dépendances
├── .env.example        # Variables d'environnement
├── .streamlit/         # Configuration Streamlit
│   └── config.toml
└── DEPLOYMENT.md       # Guide de déploiement complet
```

## 🌐 Déploiement

Voir [DEPLOYMENT.md](DEPLOYMENT.md) pour un guide complet de déploiement sur Streamlit Cloud.

## 🛠️ Technologie

- **Frontend**: Streamlit (Python)
- **IA**: Groq API (Llama 3)
- **Session**: Streamlit Session State
- **Data**: Python Dictionary (extensible à DB)

## 📊 Roadmap

- [x] MVP FREE - Chatbot IA
- [x] STANDARD - Quiz & Tracking
- [ ] PREMIUM - Phishing Simulation
- [ ] Dashboard Admin
- [ ] Intégration LDAP/AD
- [ ] Export rapports PDF
- [ ] API REST publique
- [ ] Mobile app

## 📞 Support

- **Email**: support@cybercoach.fr
- **Web**: www.cybercoach.fr

## 📄 Licence

Propriétaire - CyberCoach 2024

## ✍️ Auteurs

- Équipe CyberCoach
