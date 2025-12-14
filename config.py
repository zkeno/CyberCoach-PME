"""Configuration CyberCoach"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model
GROQ_MODEL = "llama3-8b-8192"

# System Prompt for CyberCoach
CYBERCOACH_SYSTEM_PROMPT = """Tu es CyberCoach, un assistant IA spécialisé en cybersécurité et conformité pour les PME.

**Ton Rôle:**
- Éduquer les employés aux bonnes pratiques de sécurité
- Répondre avec clarté, bienveillance et concision
- Adapter ton langage au niveau technique de l'utilisateur
- Proposer des actions concrètes et réalistes

**Domaines d'Expertise:**
- Gestion des mots de passe et authentification
- Reconnaissance et prévention du phishing
- Sécurité du télétravail
- Protection des données sensibles
- Gestion des ransomwares
- Conformité RGPD/CNIL

**Style:**
- Professionnelle mais accessible
- Pas de jargon inutile
- Exemples concrets du quotidien en entreprise
- Encourage les questions et les retours

Réponds toujours en français."""

# Quiz Config
QUIZZES = {
    "phishing": {
        "title": "Reconnaître et prévenir le phishing",
        "description": "Apprenez à identifier les emails de phishing et les techniques d'usurpation d'identité.",
        "questions": [
            {
                "id": 1,
                "question": "Vous recevez un email prétendant être de votre banque vous demandant de cliquer pour 'vérifier votre compte'. Que faites-vous ?",
                "options": [
                    "Cliquez immédiatement pour éviter les problèmes",
                    "Contactez directement votre banque par un numéro officiel",
                    "Répondez à l'email avec vos identifiants",
                    "Supprimez simplement l'email"
                ],
                "correct": 1,
                "explanation": "Contactez toujours directement l'organisme par un canal officiel. Les vraies banques ne demandent jamais les identifiants par email."
            },
            {
                "id": 2,
                "question": "Quel est le signe d'alerte principal d'un email de phishing ?",
                "options": [
                    "L'adresse email qui semble légitime",
                    "Les fautes d'orthographe et l'urgence excessive",
                    "Un attachement PDF",
                    "Un logo professionnel"
                ],
                "correct": 1,
                "explanation": "Les phisheurs font des fautes et créent une urgence artificielle pour contourner votre prudence naturelle."
            }
        ]
    },
    "passwords": {
        "title": "Gestion sécurisée des mots de passe",
        "description": "Maîtrisez les bonnes pratiques pour créer et protéger vos mots de passe.",
        "questions": [
            {
                "id": 1,
                "question": "Quel est un bon mot de passe ?",
                "options": [
                    "123456",
                    "VotreNom2024",
                    "P@ssw0rd$Sec!T2024",
                    "password"
                ],
                "correct": 2,
                "explanation": "Un bon mot de passe contient majuscules, minuscules, chiffres, caractères spéciaux et a au minimum 12 caractères."
            }
        ]
    },
    "ransomware": {
        "title": "Protection contre les ransomwares",
        "description": "Comprenez les ransomwares et comment vous protéger.",
        "questions": [
            {
                "id": 1,
                "question": "Qu'est-ce qu'un ransomware ?",
                "options": [
                    "Un virus qui ralentit votre ordinateur",
                    "Un logiciel qui chiffre vos données et demande une rançon pour les déverrouiller",
                    "Un programme publicitaire",
                    "Une mise à jour système"
                ],
                "correct": 1,
                "explanation": "Les ransomwares chiffrent vos données pour les rendre inaccessibles et demandent une rançon pour les récupérer."
            }
        ]
    },
    "telework": {
        "title": "Sécurité du télétravail",
        "description": "Travaillez de manière sécurisée en dehors du bureau.",
        "questions": [
            {
                "id": 1,
                "question": "Quel est le risque principal du télétravail ?",
                "options": [
                    "La faiblesse de la connexion internet",
                    "L'accès aux réseaux WiFi publics non sécurisés",
                    "Les mises à jour trop fréquentes",
                    "La lenteur du VPN"
                ],
                "correct": 1,
                "explanation": "Les réseaux WiFi publics (cafés, aéroports) peuvent être surveillés. Utilisez toujours un VPN ou le hotspot de votre téléphone."
            }
        ]
    }
}

# Departments (for tracking)
DEPARTMENTS = ["IT", "RH", "Finance", "Ventes", "Opérations", "Management"]
