## Setup Développeur (rapide)

Pour supprimer les avertissements d'imports manquants dans l'éditeur et exécuter l'application localement :

1. Créez et activez un environnement virtuel (recommandé) :

```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

2. Installez les dépendances :

```powershell
pip install -r requirements.txt
```

3. (Optionnel) Si votre éditeur continue d'afficher des erreurs d'import, rechargez la fenêtre ou sélectionnez l'interpréteur Python du projet (`.venv`).

4. Lancer l'app :

```powershell
streamlit run app.py
```
