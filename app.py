cat << 'EOF' > streamlit_app.py
import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

st.set_page_config(page_title="Assistente IA Avançado - Gemini", page_icon="🤖", layout="centered")

st.title("🤖 Assistente Multimodal Avançado com Gemini")
st.write("Carregue uma imagem ou vídeo, faça perguntas e mantenha uma conversa fluida com a inteligência artificial.")

# Configuração na barra lateral (Sidebar)
st.sidebar.header("⚙ Configurações")
api_key = st.sidebar.text_input("Insira sua chave API do Google Gemini", type="password")

modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo de IA", 
    ["gemini-1.5-flash", "gemini-1.5-pro"]
)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(modelo_escolhido)
    
    # Secção de upload de ficheiros na barra lateral
    st.sidebar.divider()
    st.sidebar.subheader("📎 Ficheiro Multimodal")
    arquivo_enviado = st.sidebar.file_uploader("Carregar imagem ou vídeo (opcional)", type=["jpg", "jpeg", "png", "mp4"])
    
    # Gestão do histórico de mensagens no estado da sessão
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir o histórico de mensagens anterior no chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Processar ficheiro carregado para exibir pré-visualização
    midia_para_ia = None
    if arquivo_enviado is not None:
        if arquivo_enviado.type.startswith("image"):
            imagem = Image.open(arquivo_enviado)
            st.sidebar.image(imagem, caption="Imagem carregada", use_column_width=True)
            midia_para_ia = imagem
        elif arquivo_enviado.type.startswith("video"):
            st.sidebar.video(arquivo_enviado)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(arquivo_enviado.read())
                caminho_video = temp_file.name
            with st.spinner("A processar vídeo para o Gemini..."):
                midia_para_ia = genai.upload_file(caminho_video)

    # Caixa de entrada de texto do chat na parte inferior
    if prompt := st.chat_input("Escreva a sua mensagem ou pergunta..."):
        # Adicionar mensagem do utilizador ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Gerar resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("A pensar..."):
                conteudo_pedido = []
                if midia_para_ia is not None:
                    conteudo_pedido.append(midia_para_ia)
                conteudo_pedido.append(prompt)
                
                resposta = model.generate_content(conteudo_pedido)
                st.markdown(resposta.text)
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta.text})
else:
    st.warning("⚠️ Por favor, insira a sua chave API do Google Gemini na barra lateral para começar a utilizar a aplicação.")
EOF
