@echo off
REM Lancer CyberCoach Streamlit
REM Installation des dépendances si nécessaire
pip install streamlit==1.32.0 groq==0.7.0 pandas==2.1.3 plotly==5.18.0 python-dotenv==1.0.0

REM Lancer l'app
streamlit run app.py
