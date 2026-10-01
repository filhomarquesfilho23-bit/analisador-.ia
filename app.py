import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

st.set_page_config(page_title="Analisador IA - Gemini", page_icon="🤖")

st.title("🤖 Analisador de Imagens e Vídeos com Gemini")
st.write("Carrega uma imagem ou vídeo e faz perguntas à inteligência artificial.")

api_key = st.text_input("Insere a tua Google Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    uploaded_file = st.file_uploader("Escolhe uma imagem ou vídeo...", type=["jpg", "jpeg", "png", "mp4", "mov"])
    
    if uploaded_file is not None:
        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagem carregada", use_column_width=True)
            prompt = st.text_input("O que queres perguntar sobre esta imagem?")
            if st.button("Analisar Imagem") and prompt:
                with st.spinner("A analisar a imagem..."):
                    response = model.generate_content([image, prompt])
                    st.success("Resposta:")
                    st.write(response.text)
                    
        elif uploaded_file.type.startswith("video"):
            st.video(uploaded_file)
            prompt = st.text_input("O que queres perguntar sobre este vídeo?")
            if st.button("Analisar Vídeo") and prompt:
                with st.spinner("A processar e analisar o vídeo..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(uploaded_file.read())
                        video_path = tmp.name
                    video_file = genai.upload_file(path=video_path)
                    response = model.generate_content([video_file, prompt])
                    st.success("Resposta:")
                    st.write(response.text)
else:
    st.warning("⚠️ Por favor, insere a tua chave API do Gemini para começar.")
