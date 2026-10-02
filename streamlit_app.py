
import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

st.set_page_config(page_title="Assistente IA Avançado - Gemini", page_icon="🤖")

st.title("🤖 Assistente Multimodal Avançado com Gemini")
st.write("Carregue uma imagem ou vídeo, faça perguntas e mantenha o chat interativo.")

# Configuração na barra lateral (Sidebar)
st.sidebar.header("⚙️ Configurações")
api_key = st.sidebar.text_input("Insira sua chave API do Google Gemini", type="password")

modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo de IA",
    ["gemini-3.8-flash", "gemini-3.1-pro-preview"]
)

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(modelo_escolhido)
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo: {e}")

# Secção de upload de ficheiros na barra lateral
st.sidebar.divider()
st.sidebar.subheader("📎 Ficheiro Multimodal")
arquivo_enviado = st.sidebar.file_uploader("Carregar imagem ou vídeo", type=["png", "jpg", "jpeg", "mp4"])

# Gestão do histórico de mensagens no estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir o histórico de mensagens anterior no chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do utilizador no chat
if prompt := st.chat_input("Escreva sua mensagem ou pergunta..."):
    if not api_key:
        st.warning("Por favor, insira sua chave API do Google Gemini na barra lateral.")
    else:
        # Adicionar mensagem do utilizador ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("A pensar..."):
                try:
                    conteudo_chat = []
                    
                    # Se houver imagem ou ficheiro enviado
                    if arquivo_enviado is not None:
                        imagem = Image.open(arquivo_enviado)
                        conteudo_chat.append(imagem)
                    
                    conteudo_chat.append(prompt)
                    
                    resposta = model.generate_content(conteudo_chat)
                    resposta_texto = resposta.text
                    
                    st.markdown(resposta_texto)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
