"""Module Chatbot CyberCoach utilisant Groq API"""
import streamlit as st
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, CYBERCOACH_SYSTEM_PROMPT


class CyberCoachBot:
    """Chatbot CyberCoach powered by Groq"""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY non configurée. Ajoutez-la dans .env")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def get_response(self, user_message: str, conversation_history: list) -> str:
        """
        Obtient une réponse du chatbot.
        
        Args:
            user_message: Message de l'utilisateur
            conversation_history: Historique de conversation
            
        Returns:
            Réponse du chatbot
        """
        # Ajouter le message utilisateur à l'historique
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": CYBERCOACH_SYSTEM_PROMPT}
                ] + messages,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur lors de la connexion à l'API Groq: {str(e)}"

    def initialize_session(self):
        """Initialise la session de chat dans Streamlit"""
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_chat(self):
        """Affiche l'historique du chat"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def handle_user_input(self):
        """Gère l'entrée utilisateur et affiche la réponse"""
        if prompt := st.chat_input("Posez votre question en cybersécurité..."):
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # Obtenir la réponse du chatbot
            conversation_history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages[:-1]
            ]

            response = self.get_response(prompt, conversation_history)

            # Ajouter la réponse du chatbot
            st.session_state.messages.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)


def render_chatbot_page():
    """Rendu de la page Chatbot"""
    st.header("🤖 CyberCoach - Chatbot d'IA")
    st.write(
        "Posez vos questions sur la cybersécurité et les bonnes pratiques de sécurité informatique."
    )

    bot = CyberCoachBot()
    bot.initialize_session()
    bot.display_chat()
    bot.handle_user_input()
