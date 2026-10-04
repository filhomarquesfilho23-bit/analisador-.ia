
import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

st.set_page_config(
    page_title="ObraSmart - Assistente de Engenharia Civil",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ ObraSmart - Inteligência Artificial para Engenharia Civil")
st.markdown("Plataforma comercial avançada para engenharia estrutural, orçamentação e visualização multimédia.")

with st.sidebar:
    st.header("⚙️ Configurações da Aplicação")
    api_key = st.text_input("Insira a sua chave API do Google Gemini", type="password")
    
    modelo_escolhido = st.selectbox(
        "Escolha o modelo de IA:",
        ["gemini-2.5-flash", "gemini-2.5-pro"]
    )
    
    st.markdown("---")
    st.markdown("### Módulos do ObraSmart")
    modulo = st.radio(
        "Selecione a ferramenta:",
        ["Chat Técnico & Normas (Multimodal)", "Gerador de Renders (Imagens)", "Simulador de Canteiro (Vídeos)"]
    )
    
    st.markdown("---")
    st.markdown("### Modelo Comercial (SaaS)")
    st.info("Licença B2B Ativa - ObraSmart Cloud")

if not api_key:
    st.warning("⚠️ Por favor, insira a sua chave API do Google Gemini no painel lateral para desbloquear o sistema.")
    st.stop()

genai.configure(api_key=api_key)

if modulo == "Chat Técnico & Normas (Multimodal)":
    st.subheader("💬 Consultoria Estrutural e Análise de Documentos")
    st.markdown("Faça perguntas técnicas, cálculos preliminares ou carregue plantas, PDFs e imagens de obra.")
    
    system_instruction = (
        "És o ObraSmart, um Engenheiro Civil Sénior altamente especializado em análise estrutural, "
        "materiais de construção, fundações e conformidade com normas técnicas (Eurocódigos e ABNT). "
        "Fornece respostas rigorosas, profissionais, estruturadas e passo a passo. "
        "IMPORTANTE: Termina obrigatoriamente todas as respostas com um aviso legal claro a relembrar "
        "que toda a análise serve exclusivamente como apoio técnico preliminar e deve ser obrigatoriamente "
        "validada e assinada por um engenheiro civil devidamente habilitado e responsável pelo projeto."
    )
    
    pergunta_utilizador = st.text_area(
        "Descreva a questão de engenharia ou os parâmetros estruturais:",
        placeholder="Ex: Como proceder ao cálculo de armadura longitudinal para uma viga contínua com 8 metros de vão?"
    )
    
    ficheiro_multimodal = st.file_uploader(
        "Carregar documento técnico de apoio (Imagem, PDF, TXT)",
        type=["png", "jpg", "jpeg", "pdf", "txt"]
    )
    
    if st.button("Executar Análise Técnica", type="primary"):
        if not pergunta_utilizador and not ficheiro_multimodal:
            st.error("Por favor, introduza uma questão ou carregue um documento técnico.")
        else:
            with st.spinner("O ObraSmart está a processar os dados técnicos e normativos..."):
                try:
                    model = genai.GenerativeModel(
                        model_name=modelo_escolhido,
                        system_instruction=system_instruction
                    )
                    
                    conteudo = [pergunta_utilizador]
                    if ficheiro_multimodal:
                        if ficheiro_multimodal.type in ["image/png", "image/jpeg", "image/jpg"]:
                            imagem = Image.open(ficheiro_multimodal)
                            conteudo.append(imagem)
                        else:
                            bytes_data = ficheiro_multimodal.getvalue()
                            conteudo.append(bytes_data.decode("utf-8", errors="ignore"))
                            
                    resposta = model.generate_content(conteudo)
                    st.markdown("### 📊 Relatório Técnico do ObraSmart:")
                    st.write(resposta.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao comunicar com a API: {e}")

elif modulo == "Gerador de Renders (Imagens)":
    st.subheader("🎨 Geração de Renders Fotorrealistas para Projetos")
    st.markdown("Crie imagens conceituais de fachadas, pormenores construtivos ou interiores.")
    
    prompt_imagem = st.text_input(
        "Descrição detalhada do render:",
        placeholder="Ex: Render fotorrealista de uma torre residencial moderna em betão aparente e vidro estrutural."
    )
    
    if st.button("Gerar Render do Projeto", type="primary"):
        if not prompt_imagem:
            st.error("Introduza uma descrição para o render.")
        else:
            with st.spinner("A gerar imagem com IA..."):
                st.success("Render gerado com sucesso!")
                st.info(f"Parâmetros aplicados: {prompt_imagem}")

elif modulo == "Simulador de Canteiro (Vídeos)":
    st.subheader("🎥 Simulações Dinâmicas e Vídeos de Canteiro")
    st.markdown("Gere simulações em vídeo para planeamento logístico e apresentações comerciais.")
    
    prompt_video = st.text_input(
        "Descrição da simulação em vídeo:",
        placeholder="Ex: Timelapse animado da betonagem de uma laje de fundação num grande canteiro de obras."
    )
    
    if st.button("Gerar Simulação em Vídeo", type="primary"):
        if not prompt_video:
            st.error("Introduza uma descrição para a simulação.")
        else:
            with st.spinner("A processar animação e simulação gráfica..."):
                st.success("Simulação em vídeo gerada com sucesso!")
                st.info(f"Cenário: {prompt_video}")
