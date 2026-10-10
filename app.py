import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis de ambiente (.env) se estiver rodando localmente
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(
    page_title="EstudaAI — Tutor Inteligente",
    page_icon="🎓",
    layout="wide"
)

# ----- CSS ULTRA-CUSTOMIZADO (DESIGN PREMIUM) -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 900px;
    }

    .hero-card {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
        margin-bottom: 2rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
    }

    .hero-subtitle {
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.9;
        margin: 0;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.15);
        padding-top: 1rem;
    }

    .badge-wrapper {
        display: flex;
        gap: 10px;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }

    .custom-badge {
        background: rgba(37, 99, 235, 0.1);
        border: 1px solid rgba(37, 99, 235, 0.25);
        color: #2563EB;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 18px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
    }

    .stSelectbox div[data-baseweb="select"], .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid rgba(128, 128, 128, 0.25) !important;
    }

    div[data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 2px solid rgba(37, 99, 235, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        background-color: var(--secondary-background-color);
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização da chave da API Groq
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("🔑 A chave `GROQ_API_KEY` não foi encontrada. Configure nas variáveis de ambiente.")
    st.stop()

client = Groq(api_key=api_key)

# ----- BARRA LATERAL (PAINEL DE CONTROLE) -----
with st.sidebar:
    st.markdown("### 🎓 Painel EstudaAI")
    st.caption("Personalize a inteligência do seu tutor.")
    
    st.markdown("---")

    modo = st.selectbox(
        "🎯 Modo de Atendimento:",
        [
            "💡 Explicar Conceito (ELI5)",
            "📝 Resumo Estruturado",
            "❓ Quiz de Fixação",
            "📅 Cronograma de Estudos",
            "💬 Dúvida Livre"
        ]
    )

    nivel = st.selectbox(
        "⚡ Nível de Complexidade:",
        [
            "🟢 Fácil (Iniciante)",
            "🟡 Médio (Intermediário)",
            "🔴 Difícil (Avançado)"
        ]
    )

    st.markdown("---")
    
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray; font-size: 0.8rem;'>Feito com Python, Streamlit e Groq API</div>", unsafe_allow_html=True)

modo_limpo = modo.split(" ", 1)[1]
nivel_limpo = nivel.split(" ", 1)[1]

# PROMPTS DO SISTEMA
PROMPTS_SISTEMA = {
    "Explicar Conceito (ELI5)": (
        f"Você é um tutor acadêmico extremamente didático. O nível desejado é: {nivel_limpo}. "
        "Explique o assunto solicitado de forma clara e organizada por tópicos."
    ),
    "Resumo Estruturado": (
        f"Você é um especialista em síntese acadêmica. O nível de profundidade é: {nivel_limpo}. "
        "Gere um resumo estruturado contendo: 1. Conceitos Chave; 2. Pontos Críticos; 3. Conclusão Prática."
    ),
    "Quiz de Fixação": (
        f"Você é um elaborador de exames. Crie um quiz interativo com 3 perguntas de múltipla escolha (A, B, C, D) "
        f"adequadas ao nível: {nivel_limpo}.\n\n"
        "REGRA OBRIGATÓRIA DE FORMATO:\n"
        "Apresente primeiro APENAS as 3 perguntas e suas alternativas.\n"
        "No final do texto, coloque a palavra chave '---GABARITO---' e, abaixo dela, escreva as respostas e o gabarito comentado."
    ),
    "Cronograma de Estudos": (
        f"Você é um mentor de produtividade. Crie um plano de estudos prático e estruturado para o nível: {nivel_limpo}."
    ),
    "Dúvida Livre": (
        f"Você é um assistente acadêmico de elite. Responda à dúvida adaptando o tom para o nível: {nivel_limpo}."
    )
}

# ----- CORPO PRINCIPAL DA APLICAÇÃO -----
st.markdown("""
    <div class="hero-card">
        <h1 class="hero-title">🎓 EstudaAI</h1>
        <p class="hero-subtitle">Seu assistente inteligente de estudos impulsionado por IA.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="badge-wrapper">
        <span class="custom-badge">🎯 Modo: {modo_limpo}</span>
        <span class="custom-badge">⚡ Nível: {nivel_limpo}</span>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    avatar_user = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_user):
        content = message["content"]
        # Se for uma mensagem do assistente contendo o separador do gabarito, esconde o gabarito num expander
        if message["role"] == "assistant" and "---GABARITO---" in content:
            partes = content.split("---GABARITO---")
            st.markdown(partes[0].strip())
            with st.expander("🔍 Clique aqui para ver o Gabarito e Explicações"):
                st.markdown(partes[1].strip())
        else:
            st.markdown(content)

# Entrada do usuário
if prompt := st.chat_input("Digite o assunto, cole seu texto ou faça uma pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    system_message = {"role": "system", "content": PROMPTS_SISTEMA[modo_limpo]}
    user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    mensagens_finais = [system_message] + user_messages

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("✨ O EstudaAI está preparando a resposta perfeita para você..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=mensagens_finais,
                )
                resposta = chat_completion.choices[0].message.content
                
                # Trata a exibição do gabarito em um expander escondido
                if "---GABARITO---" in resposta:
                    partes = resposta.split("---GABARITO---")
                    st.markdown(partes[0].strip())
                    with st.expander("🔍 Clique aqui para ver o Gabarito e Explicações"):
                        st.markdown(partes[1].strip())
                else:
                    st.markdown(resposta)
                
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a Groq: {e}")
