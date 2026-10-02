
import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

st.set_page_config(page_title="Assistente IA Avançado - Gemini", page_icon="🤖")

st.title("🤖 Assistente Multimodal Avançado com Gemini")
st.write("Carregue ficheiros (imagens, vídeos, PDFs, TXT, CSV), faça perguntas e gerencie o seu chat.")

# Configuração na barra lateral (Sidebar)
st.sidebar.header("⚙️ Configurações")
api_key = st.sidebar.text_input("Insira sua chave API do Google Gemini", type="password")

modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo de IA",
    ["gemini-3.8-flash", "gemini-3.1-pro-preview"]
)

# 1. Controlo de Criatividade (Temperatura)
temperatura = st.sidebar.slider(
    "🌡️ Criatividade (Temperatura)", 
    0.0, 1.0, 0.7, 
    help="Valores baixos = respostas diretas e precisas. Valores altos = respostas mais criativas."
)

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(modelo_escolhido)
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo: {e}")

# Secção de upload de ficheiros na barra lateral (4. Suporte a Documentos, Imagens, Vídeos)
st.sidebar.divider()
st.sidebar.subheader("📎 Ficheiro Multimodal")
arquivo_enviado = st.sidebar.file_uploader(
    "Carregar ficheiro (Imagem, Vídeo, PDF, TXT, CSV)", 
    type=["png", "jpg", "jpeg", "mp4", "pdf", "txt", "csv"]
)

# Gestão do histórico de mensagens no estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Botão para Limpar o Chat
if st.sidebar.button("🗑️ Limpar Conversa"):
    st.session_state.messages = []
    st.rerun()

# 3. Exportar o Histórico da Conversa
if st.session_state.messages:
    chat_texto = ""
    for m in st.session_state.messages:
        chat_texto += f"{m['role'].upper()}: {m['content']}\n\n"
    st.sidebar.download_button(
        label="📥 Baixar Conversa (.txt)",
        data=chat_texto,
        file_name="historico_conversa.txt",
        mime="text/plain"
    )

st.sidebar.divider()

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
                    
                    # Processamento inteligente de ficheiros enviados
                    if arquivo_enviado is not None:
                        ext = arquivo_enviado.name.split('.')[-1].lower()
                        if ext in ["png", "jpg", "jpeg"]:
                            imagem = Image.open(arquivo_enviado)
                            conteudo_chat.append(imagem)
                        elif ext in ["txt", "csv"]:
                            texto_doc = arquivo_enviado.getvalue().decode("utf-8")
                            conteudo_chat.append(f"Conteúdo do documento ({arquivo_enviado.name}):\n{texto_doc}")
                        else:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                                tmp.write(arquivo_enviado.getvalue())
                                tmp_path = tmp.name
                            file_ref = genai.upload_file(tmp_path)
                            conteudo_chat.append(file_ref)
                    
                    conteudo_chat.append(prompt)
                    
                    # Gerar resposta com a temperatura configurada
                    generation_config = {"temperature": temperatura}
                    resposta = model.generate_content(conteudo_chat, generation_config=generation_config)
                    resposta_texto = resposta.text
                    
                    st.markdown(resposta_texto)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
