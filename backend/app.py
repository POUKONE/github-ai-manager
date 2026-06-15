import streamlit as st
import os
import sys
import dotenv

# Configuration du chemin pour importer tes modules
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import des composants de ton projet existant et de la pipeline
from main_pipeline import run_agent_pipeline

dotenv.load_dotenv()

# Configuration de la page web
st.set_page_config(
    page_title="GitHub AI Manager 🤖",
    page_icon="🤖",
    layout="wide"
)

# --- DIRECTIVE ULTRA DESIGN & EDGE : INJECTION DE L'ARCHITECTURE GRAPHIQUE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;800&family=JetBrains+Mono:wght=400;700&display=swap');
        
        /* [ULTRA DESIGN] Force l'affichage et la lisibilité globale */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
            background-color: #050508 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #F8FAFC !important;
        }
        
        /* Ajustement du filigrane : z-index mis à -1 pour ne pas bloquer l'affichage */
        [data-testid="stAppViewContainer"]::before {
            content: "POUKONE YOGNE IBRAHIMA";
            position: fixed;
            bottom: 30px;
            right: 30px;
            font-size: 3.5rem;
            font-weight: 800;
            color: rgba(255, 255, 255, 0.03) !important;
            z-index: -1 !important;
            pointer-events: none;
            letter-spacing: 2px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* [EDGE] Dissociation spatiale du panneau latéral */
        [data-testid="stSidebar"] {
            background-color: #0B0B14 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Titre principal */
        .brand-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -1.5px;
            background: linear-gradient(135deg, #FFFFFF 30%, #64748B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            display: block;
        }
        
        .brand-subtitle {
            font-size: 1rem;
            color: #94A3B8;
            font-weight: 400;
            margin-bottom: 2.5rem;
            letter-spacing: -0.2px;
            display: block;
        }
        
        /* Panneaux */
        .glass-panel {
            background: rgba(15, 15, 25, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1rem;
        }
        
        /* Boutons d'action */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
        }

        /* Console */
        .terminal-shell {
            background-color: #020204;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .terminal-topbar {
            background-color: #0D0D15;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        .window-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
            display: inline-block;
        }
        .w-red { background-color: #EF4444; }
        .w-yellow { background-color: #F59E0B; }
        .w-green { background-color: #10B981; }
        
        .terminal-tab {
            color: #64748B;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            margin-left: 15px;
        }
        
        .log-row {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
            padding: 6px 16px;
            margin: 4px 0;
        }
        .log-info { color: #93C5FD; }
        .log-success { color: #6EE7B7; }
        .log-warning { color: #FCD34D; }
        .log-error { color: #FCA5A5; }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown('<div class="brand-title">GitHub AI Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">Moteur d\'orchestration multi-agents autonome • Pipeline de production SecOps / FinOps</div>', unsafe_allow_html=True)

# --- CONFIGURATION SIDEBAR ---
github_token = os.getenv("GITHUB_TOKEN", "")
openai_key = os.getenv("OPENAI_API_KEY", "")

st.sidebar.markdown("<br><h2 style='letter-spacing:-1px; color:#F8FAFC; font-weight:800; font-size:1.6rem;'>📚 Connaissances Centrales (RAG)</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;'>Base de connaissances statique injectée directement au cœur des agents.</p>", unsafe_allow_html=True)

rag_path = os.path.join(backend_dir, "config", "coding_rules.txt")
if os.path.exists(rag_path):
    with open(rag_path, "r", encoding="utf-8") as f:
        rules_preview = f.read()
    st.sidebar.markdown("<p style='font-weight:600; font-size:1rem; color:#E2E8F0; margin-bottom:0.5rem;'>Règles de contexte actives :</p>", unsafe_allow_html=True)
    st.sidebar.code(rules_preview, language="text")
else:
    st.sidebar.warning("⚠️ Fichier coding_rules.txt manquant")

# --- PANNEAU PRINCIPAL ---
col1, col2 = st.columns([1, 1.6], gap="large")

with col1:
    st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#F8FAFC; margin-bottom:1rem;">⚙️ Matrice de Ciblage</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    repo_target = st.text_input("Dépôt GitHub à auditer", value="POUKONE/sandbox-ai")
    budget_max = st.slider("Seuil d'interception FinOps (Tokens)", min_value=500, max_value=3000, value=1500)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn_lancer = st.button("🚀 EXÉCUTER LA PIPELINE", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#F8FAFC; margin-bottom:1rem;">📈 Métriques Opérationnelles</p>', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Protection FinOps", value=f"{budget_max} tkn")
    with m_col2:
        st.metric(label="État de la Pipeline", value="Active" if btn_lancer else "En attente")

with col2:
    st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#F8FAFC; margin-bottom:1rem;">📟 Console d\'Orchestration des Agents</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="terminal-shell">
            <div class="terminal-topbar">
                <span class="window-dot w-red"></span>
                <span class="window-dot w-yellow"></span>
                <span class="window-dot w-green"></span>
                <span class="terminal-tab">multi-agent-orchestrator@engine:~</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    log_container = st.container(border=False)

    def update_gui_logs(message, type_log="info"):
        with log_container:
            if type_log == "success":
                st.markdown(f'<div class="log-row log-success">✔ [SUCCÈS] {message}</div>', unsafe_allow_html=True)
            elif type_log == "warning":
                st.markdown(f'<div class="log-row log-warning">⚠ [AVERTISSEMENT] {message}</div>', unsafe_allow_html=True)
            elif type_log == "error":
                st.markdown(f'<div class="log-row log-error">✖ [CRITIQUE] {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="log-row log-info">⚡ [SYSTÈME] {message}</div>', unsafe_allow_html=True)

    if btn_lancer:
        if not github_token or not openai_key:
            st.error("🔒 Extraction impossible : Variables d'infrastructure manquantes.")
        else:
            with st.spinner(""):
                success, report = run_agent_pipeline(
                    token=github_token,
                    openai_key=openai_key,
                    target_repo=repo_target,
                    max_budget=budget_max,
                    log_callback=update_gui_logs
                )
                
                if success:
                    st.toast("Pipeline validée !", icon="🚀")
                    st.balloons()
                    st.markdown("<br>### 📄 Compilation du rapport d'audit", unsafe_allow_html=True)
                    st.code(report, language="text")
                else:
                    st.error("💥 Interception : Échec de la boucle d'auto-correction.")
                    with st.expander("Consulter le rapport de crash complet"):
                        st.code(report, language="text")
    else:
        with log_container:
            st.markdown('<div class="log-row log-info" style="color: #64748B;">En attente du signal d\'initialisation... Cliquez sur "EXÉCUTER LA PIPELINE".</div>', unsafe_allow_html=True)