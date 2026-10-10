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

# ----- CSS ULTRA-CUSTOMIZADO (DESIGN PREMIUM & PROFISSIONAL) -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Aplicando fonte global */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Ocultar elementos padrão do Streamlit para um visual limpo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Container Principal */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 900px;
    }

    /* Cartão de Cabeçalho (Hero Header) */
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

    /* Estilização da Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: var(--background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.15);
        padding-top: 1rem;
    }

    /* Badges de Status Modernas */
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

    /* Balões de Chat Estilizados */
    div[data-testid="stChatMessage"] {
        border-radius: 18px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease;
    }

    /* Campos de Seleção e Inputs na Sidebar */
    .stSelectbox div[data-baseweb="select"], .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid rgba(128, 128, 128, 0.25) !important;
    }

    /* Caixa de Input de Chat Flutuante */
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

    # Seletor de Modo
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

    # Seletor de Nível de Dificuldade
    nivel = st.selectbox(
        "⚡ Nível de Complexidade:",
        [
            "🟢 Fácil (Iniciante)",
            "🟡 Médio (Intermediário)",
            "🔴 Difícil (Avançado)"
        ]
    )

    st.markdown("---")
    
    # Botão de limpar conversa para facilitar testes
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray; font-size: 0.8rem;'>Feito com Python, Streamlit e Groq API</div>", unsafe_allow_html=True)

# Limpeza das tags para uso nos prompts da IA
modo_limpo = modo.split(" ", 1)[1]
nivel_limpo = nivel.split(" ", 1)[1]

# PROMPTS DO SISTEMA (ENGENHARIA DE PROMPT PROFISSIONAL)
PROMPTS_SISTEMA = {
    "Explicar Conceito (ELI5)": (
        f"Você é um tutor acadêmico extremamente didático. O nível de complexidade desejado é: {nivel_limpo}. "
        "Explique o assunto solicitado de forma clara, utilizando analogias do mundo real se o nível for fácil, "
        "ou termos técnicos aprofundados se for avançado. Mantenha uma estrutura organizada com tópicos."
    ),
    "Resumo Estruturado": (
        f"Você é um especialista em síntese e técnicas de estudo ativas. O nível de profundidade deve ser: {nivel_limpo}. "
        "Gere um resumo estruturado contendo obrigatoriamente: 1. Conceitos Chave; 2. Pontos Críticos de Atenção; 3. Conclusão Prática."
    ),
    "Quiz de Fixação": (
        f"Você é um elaborador de exames pedagógicos. Crie um quiz interativo com 3 perguntas de múltipla escolha (A, B, C, D) "
        f"adequadas ao nível: {nivel_limpo}. No final da resposta, inclua o gabarito detalhado e comentado para cada questão."
    ),
    "Cronograma de Estudos": (
        f"Você é um mentor de alta performance e produtividade. Crie um plano de estudos prático, passo a passo e estruturado "
        f"com base no nível: {nivel_limpo}, otimizando o tempo de aprendizado do aluno."
    ),
    "Dúvida Livre": (
        f"Você é um assistente acadêmico polivalente de elite. Responda à dúvida apresentada com precisão rigorosa, "
        f"clareza pedagógica e adaptando o tom para o nível: {nivel_limpo}."
    )
}

# ----- CORPO PRINCIPAL DA APLICAÇÃO (HEADER VISUAL) -----
st.markdown("""
    <div class="hero-card">
        <h1 class="hero-title">🎓 EstudaAI</h1>
        <p class="hero-subtitle">Seu assistente inteligente de estudos impulsionado por inteligência artificial avançada.</p>
    </div>
""", unsafe_allow_html=True)

# Badges visuais indicando o estado atual do agente
st.markdown(f"""
    <div class="badge-wrapper">
        <span class="custom-badge">🎯 Modo: {modo_limpo}</span>
        <span class="custom-badge">⚡ Nível: {nivel_limpo}</span>
    </div>
""", unsafe_allow_html=True)

# Inicialização do histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens com avatares customizados
for message in st.session_state.messages:
    avatar_user = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_user):
        st.markdown(message["content"])

# Entrada do usuário (Chat Input flutuante)
if prompt := st.chat_input("Digite o assunto,cole seu texto ou faça uma pergunta..."):
    # Salva e mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Prepara o contexto do sistema com base na engenharia de prompt
    system_message = {"role": "system", "content": PROMPTS_SISTEMA[modo_limpo]}
    user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    mensagens_finais = [system_message] + user_messages

    # Chamada para a API da Groq com animação de carregamento elegante
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("✨ O EstudaAI está preparando a melhor explicação para você..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=mensagens_finais,
                )
                resposta = chat_completion.choices[0].message.content
                st.markdown(resposta)
                
                # Salva a resposta no histórico da sessão
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a Groq: {e}")
