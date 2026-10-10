import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis de ambiente (.env) se estiver rodando localmente
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(
    page_title="EstudaAI - Agente de Estudos",
    page_icon="🎓",
    layout="wide"
)

# Inicialização da chave da API Groq
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("🔑 A chave `GROQ_API_KEY` não foi encontrada. Configure nas variáveis de ambiente.")
    st.stop()

client = Groq(api_key=api_key)

# ----- BARRA LATERAL (CONFIGURAÇÕES E MODOS) -----
st.sidebar.title("🎓 EstudaAI")
st.sidebar.markdown("Seu tutor inteligente para otimizar aprendizado e rotina.")

# Seletor de Modo
modo = st.sidebar.selectbox(
    "Escolha o modo de atendimento:",
    [
        "Explicar Conceito Simplificado (ELI5)",
        "Gerar Resumo Focado",
        "Criar Quiz de Fixação (3 Perguntas)",
        "Planejar Rotina de Estudos",
        "Dúvida Livre"
    ]
)

# NOVO: Seletor de Nível de Dificuldade
st.sidebar.markdown("---")
nivel = st.sidebar.selectbox(
    "Escolha o nível de complexidade:",
    [
        "Fácil (Iniciante / Didático)",
        "Médio (Intermediário / Padrão)",
        "Difícil (Avançado / Técnico e Aprofundado)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** O nível escolhido ajusta automaticamente a profundidade das respostas da IA!")

# PROMPTS DO SISTEMA DE ACORDO COM O MODO E O NÍVEL SELECIONADO
PROMPTS_SISTEMA = {
    "Explicar Conceito Simplificado (ELI5)": (
        f"Você é um tutor acadêmico extremamente didático. O nível de complexidade desejado para a explicação é: {nivel}. "
        "Explique o assunto de acordo com este nível (se fácil, use muitas metáforas simples; se difícil, use termos técnicos rigurosos)."
    ),
    "Gerar Resumo Focado": (
        f"Você é um especialista em síntese. O nível do resumo deve ser: {nivel}. "
        "Gere um resumo estruturado contendo: 1. Conceitos Chave; 2. Pontos de Atenção; 3. Conclusão Principal."
    ),
    "Criar Quiz de Fixação (3 Perguntas)": (
        f"Você é um elaborador de exames. Crie um quiz com 3 perguntas de múltipla escolha (A, B, C, D) "
        f"com o grau de dificuldade adequado ao nível: {nivel}. No final, forneça o gabarito comentado."
    ),
    "Planejar Rotina de Estudos": (
        f"Você é um especialista em produtividade. Crie um plano de estudos prático, estruturado e com foco no nível: {nivel}."
    ),
    "Dúvida Livre": (
        f"Você é um assistente acadêmico polivalente. Responda à dúvida do usuário adaptando a profundidade da resposta para o nível: {nivel}."
    )
}

# ----- CORPO PRINCIPAL DA APLICAÇÃO -----
st.title("🎓 EstudaAI — Tutor Inteligente")
st.caption(f"Modo atual: **{modo}** | Nível selecionado: **{nivel}**")

# Inicialização do histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite o assunto, pergunta ou texto para análise..."):
    # Salva e mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara a chamada para a API com a engenharia de prompt atualizada com o nível
    system_message = {"role": "system", "content": PROMPTS_SISTEMA[modo]}
    user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    mensagens_finais = [system_message] + user_messages

    # Chamada para a API da Groq
    with st.chat_message("assistant"):
        with st.spinner("O EstudaAI está processando sua resposta..."):
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
