import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis de ambiente (.env) se estiver rodando localmente
load_dotenv()

# Configuração da página do Streamlit (deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="EstudaAI - Tutor Inteligente",
    page_icon="🎓",
    layout="wide"
)

# ----- ESTILO CSS PERSONALIZADO (DEIXANDO TUDO MAIS BONITO) -----
st.markdown("""
    <style>
    /* Estilo geral da página */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Título principal */
    h1 {
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    
    /* Ajuste da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Caixas de texto e selects */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
        border-radius: 8px;
    }
    
    /* Botões e inputs */
    .stTextInput input {
        border-radius: 8px;
    }
    
    /* Mensagens do chat */
    div.stChatMessage {
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização da chave da API Groq
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("🔑 A chave `GROQ_API_KEY` não foi encontrada. Configure nas variáveis de ambiente.")
    st.stop()

client = Groq(api_key=api_key)

# ----- BARRA LATERAL (CONFIGURAÇÕES E MODOS) -----
st.sidebar.title("🎓 EstudaAI")
st.sidebar.markdown("Seu tutor inteligente para otimizar aprendizado e rotina.")

st.sidebar.markdown("---")

# Seletor de Modo com ícones visuais
modo = st.sidebar.selectbox(
    "🎯 Modo de Atendimento:",
    [
        "💡 Explicar Conceito Simplificado (ELI5)",
        "📝 Gerar Resumo Focado",
        "❓ Criar Quiz de Fixação (3 Perguntas)",
        "📅 Planejar Rotina de Estudos",
        "💬 Dúvida Livre"
    ]
)

# Seletor de Nível de Dificuldade
nivel = st.sidebar.selectbox(
    "⚡ Nível de Complexidade:",
    [
        "🟢 Fácil (Iniciante / Didático)",
        "🟡 Médio (Intermediário / Padrão)",
        "🔴 Difícil (Avançado / Técnico)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** O nível e o modo ajustam automaticamente a IA para o seu objetivo!")

# Limpa o texto dos emojis para usar no prompt da IA
modo_limpo = modo.split(" ", 1)[1]
nivel_limpo = nivel.split(" ", 1)[1]

# PROMPTS DO SISTEMA DE ACORDO COM O MODO E O NÍVEL
PROMPTS_SISTEMA = {
    "Explicar Conceito Simplificado (ELI5)": (
        f"Você é um tutor acadêmico extremamente didático. O nível desejado é: {nivel_limpo}. "
        "Explique o assunto de forma clara, engajadora e estruturada."
    ),
    "Gerar Resumo Focado": (
        f"Você é um especialista em síntese. O nível do resumo deve ser: {nivel_limpo}. "
        "Gere um resumo estruturado contendo: 1. Conceitos Chave; 2. Pontos de Atenção; 3. Conclusão Principal."
    ),
    "Criar Quiz de Fixação (3 Perguntas)": (
        f"Você é um elaborador de exames. Crie um quiz com 3 perguntas de múltipla escolha (A, B, C, D) "
        f"com o grau de dificuldade adequado ao nível: {nivel_limpo}. No final, forneça o gabarito comentado."
    ),
    "Planejar Rotina de Estudos": (
        f"Você é um especialista em produtividade. Crie um plano de estudos prático, estruturado e com foco no nível: {nivel_limpo}."
    ),
    "Dúvida Livre": (
        f"Você é um assistente acadêmico polivalente. Responda à dúvida adaptando a profundidade para o nível: {nivel_limpo}."
    )
}

# ----- CORPO PRINCIPAL DA APLICAÇÃO -----
st.title("🎓 EstudaAI — Tutor Inteligente")
st.caption(f"✨ Modo: **{modo_limpo}** | ⚡ Nível: **{nivel_limpo}**")
st.markdown("---")

# Inicialização do histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário (Chat Input moderno do Streamlit)
if prompt := st.chat_input("Digite o assunto, pergunta ou cole seu texto aqui..."):
    # Salva e mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara a chamada para a API com a engenharia de prompt atualizada
    system_message = {"role": "system", "content": PROMPTS_SISTEMA[modo_limpo]}
    user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    mensagens_finais = [system_message] + user_messages

    # Chamada para a API da Groq com animação de carregamento elegante
    with st.chat_message("assistant"):
        with st.spinner("🤖 O EstudaAI está preparando a resposta perfeita para você..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=mensagens_finais,
                )
                resposta = chat_completion.choices[0].message.content
                st.markdown(resposta)
                
                # Salva a resposta no histórico da conversa
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a Groq: {e}")
