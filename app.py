"""Application principale CyberCoach - Chatbot Cybersécurité pour PME"""
import streamlit as st
from chatbot import render_chatbot_page
from quiz import render_quiz_page

# Configuration de la page
st.set_page_config(
    page_title="CyberCoach",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .offer-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.image(
        "https://via.placeholder.com/200x60/FF6B35/FFFFFF?text=CyberCoach",
        use_column_width=True,
    )
    st.markdown("---")
    st.markdown("## 📌 Menu Principal")

    page = st.radio(
        "Sélectionnez une option:",
        ["🏠 Accueil", "🤖 Chatbot (FREE)", "📚 Quiz & Formation (STANDARD)", "� Phishing (PREMIUM)", "�🔧 Admin Dashboard"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 💡 À propos")
    st.info(
        """
        **CyberCoach** est un système intelligent de formation en cybersécurité 
        conçu pour les PME.
        
        **Transformez le risque humain en défense proactive!**
        """
    )

    st.markdown("### 📞 Support")
    st.write("Email: support@cybercoach.fr")
    st.write("Web: www.cybercoach.fr")

def render_home_page():
    """Rendu de la page d'accueil"""
    st.markdown(
        """
        # 🛡️ CyberCoach
        ## Votre Assistant IA de Cybersécurité
        
        Bienvenue sur **CyberCoach**, la plateforme complète de formation et de 
        sécurité informatique pour les PME. Transformez vos collaborateurs en première 
        ligne de défense contre les cybermenaces.
        
        ---
        
        ## 🎯 Nos Offres
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 🆓 FREE
            #### Chatbot Intelligent
            - ✅ Accès illimité au Chatbot CyberCoach
            - ✅ Questions sur la cybersécurité 24/7
            - ✅ Réponses pédagogiques et bienveillantes
            - ✅ Parfait pour commencer
            
            **Tarif: 0€/mois**
            """
        )

    with col2:
        st.markdown(
            """
            ### 💳 STANDARD
            #### Quiz & Formation
            - ✅ Quiz interactifs (Phishing, Mots de passe, etc.)
            - ✅ Suivi des progrès par collaborateur
            - ✅ Taux de complétion & Scores moyens par département
            - ✅ Rapports de conformité
            - ✅ Preuve de formation pour auditeurs
            
            **Tarif: 99€/mois**
            """
        )

    with col3:
        st.markdown(
            """
            ### 🚀 PREMIUM
            #### Gestion du Risque
            - ✅ Simulations de phishing réelles
            - ✅ Tableau de Bord Exécutif (TRV)
            - ✅ Mesure de résistance réelle
            - ✅ Remédiation instantanée
            - ✅ ROI sur investissement
            
            **Tarif: 499€/mois**
            *(Bientôt disponible)*
            """
        )

    st.markdown(
        """
        ---
        
        ## 🚀 Commencer Maintenant
        
        1. **Explorez le Chatbot** (Offre FREE) - Posez vos questions
        2. **Lancez les Quiz** (Offre STANDARD) - Formez vos équipes
        3. **Mesurez votre progression** - Suivi en temps réel
        
        ---
        
        ## 📊 Pourquoi CyberCoach ?
        
        - 🎯 **Simplifié**: Une seule plateforme pour tous vos besoins
        - 🔐 **Sécurisé**: IA spécialisée en cybersécurité
        - 📈 **Mesurable**: Rapports détaillés et KPIs clairs
        - 💰 **Rentable**: ROI démontré contre les pertes liées aux cyberattaques
        - 🌍 **Accessible**: Disponible 24/7 pour vos équipes
        
        ---
        
        **Transformez votre culture de sécurité dès aujourd'hui!**
        """
    )

# Contenu principal
if page == "🏠 Accueil":
    render_home_page()
elif page == "🤖 Chatbot (FREE)":
    render_chatbot_page()
elif page == "📚 Quiz & Formation (STANDARD)":
    render_quiz_page()
elif page == "� Phishing (PREMIUM)":
    from phishing_ui import render_phishing_page
    render_phishing_page()

elif page == "�🔧 Admin Dashboard":
    from admin import render_admin
    render_admin()


def render_home_page():
    """Rendu de la page d'accueil"""
    st.markdown(
        """
        # 🛡️ CyberCoach
        ## Votre Assistant IA de Cybersécurité
        
        Bienvenue sur **CyberCoach**, la plateforme complète de formation et de 
        sécurité informatique pour les PME. Transformez vos collaborateurs en première 
        ligne de défense contre les cybermenaces.
        
        ---
        
        ## 🎯 Nos Offres
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 🆓 FREE
            #### Chatbot Intelligent
            - ✅ Accès illimité au Chatbot CyberCoach
            - ✅ Questions sur la cybersécurité 24/7
            - ✅ Réponses pédagogiques et bienveillantes
            - ✅ Parfait pour commencer
            
            **Tarif: 0€/mois**
            """
        )

    with col2:
        st.markdown(
            """
            ### 💳 STANDARD
            #### Quiz & Formation
            - ✅ Quiz interactifs (Phishing, Mots de passe, etc.)
            - ✅ Suivi des progrès par collaborateur
            - ✅ Taux de complétion & Scores moyens par département
            - ✅ Rapports de conformité
            - ✅ Preuve de formation pour auditeurs
            
            **Tarif: 99€/mois**
            """
        )

    with col3:
        st.markdown(
            """
            ### 🚀 PREMIUM
            #### Gestion du Risque
            - ✅ Simulations de phishing réelles
            - ✅ Tableau de Bord Exécutif (TRV)
            - ✅ Mesure de résistance réelle
            - ✅ Remédiation instantanée
            - ✅ ROI sur investissement
            
            **Tarif: 499€/mois**
            *(Bientôt disponible)*
            """
        )

    st.markdown(
        """
        ---
        
        ## 🚀 Commencer Maintenant
        
        1. **Explorez le Chatbot** (Offre FREE) - Posez vos questions
        2. **Lancez les Quiz** (Offre STANDARD) - Formez vos équipes
        3. **Mesurez votre progression** - Suivi en temps réel
        
        ---
        
        ## 📊 Pourquoi CyberCoach ?
        
        - 🎯 **Simplifié**: Une seule plateforme pour tous vos besoins
        - 🔐 **Sécurisé**: IA spécialisée en cybersécurité
        - 📈 **Mesurable**: Rapports détaillés et KPIs clairs
        - 💰 **Rentable**: ROI démontré contre les pertes liées aux cyberattaques
        - 🌍 **Accessible**: Disponible 24/7 pour vos équipes
        
        ---
        
        **Transformez votre culture de sécurité dès aujourd'hui!**
        """
    )


# Appel de la fonction pour la page d'accueil (lors du premier chargement)
if page == "🏠 Accueil":
    pass  # La fonction est déjà appelée ci-dessus
