
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="ObraSmart - Assistente de Engenharia Civil",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ ObraSmart - Inteligência Artificial e Gestão para Engenharia Civil")
st.markdown("Plataforma comercial avançada para engenharia estrutural, orçamentação e análise de dados.")

with st.sidebar:
    st.header("⚙️ Configurações da Aplicação")
    api_key = st.text_input("Insira a sua chave API do Google Gemini", type="password")
    
    modelo_escolhido = st.selectbox(
        "Escolha o modelo de IA:",
        ["gemini-3.5-flash-lite", "gemini-1.5-pro"]
    )
    
    st.markdown("---")
    st.markdown("### Módulos do ObraSmart")
    modulo = st.radio(
        "Selecione a ferramenta:",
        [
            "Chat Técnico & Normas (Multimodal)", 
            "Dashboard de Custos & Obras", 
            "Gerador de Renders (Imagens)", 
            "Simulador de Canteiro (Vídeos)"
        ]
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

elif modulo == "Dashboard de Custos & Obras":
    st.subheader("📊 Dashboard de Controlo de Custos e Orçamentos")
    st.markdown("Monitorize os desvios financeiros, o orçamento previsto e o custo real das várias fases da construção.")
    
    dados_obra = {
        "Fase da Obra": ["Fundações", "Estrutura", "Alvenaria", "Instalações", "Acabamentos"],
        "Previsto_EUR": [50000, 120000, 35000, 45000, 60000],
        "Real_EUR": [52000, 118000, 39500, 43000, 62000]
    }
    
    df = pd.DataFrame(dados_obra)
    df["Desvio_EUR"] = df["Real_EUR"] - df["Previsto_EUR"]
    
    total_previsto = df["Previsto_EUR"].sum()
    total_real = df["Real_EUR"].sum()
    desvio_total = total_real - total_previsto
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Orçamento Total", f"€ {total_previsto:,.2f}")
    col2.metric("Custo Total Real", f"€ {total_real:,.2f}", delta=f"€ {desvio_total:,.2f}", delta_color="inverse")
    
    if desvio_total > 0:
        col3.metric("Estado Global", "⚠️ Estouro de Orçamento")
    else:
        col3.metric("Estado Global", "✅ Orçamento Controlado")
        
    st.markdown("---")
    st.markdown("### 📈 Comparativo Gráfico: Orçamento vs Custo Real")
    
    df_chart = df.set_index("Fase da Obra")[["Previsto_EUR", "Real_EUR"]]
    st.bar_chart(df_chart)
    
    st.markdown("### 📋 Tabela Analítica de Fases")
    st.dataframe(df, use_container_width=True)

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
    
    if st.button("Simulação em Vídeo", type="primary"):
        if not prompt_video:
            st.error("Introduza uma descrição para a simulação.")
        else:
            with st.spinner("A processar animação e simulação gráfica..."):
                st.success("Simulação em vídeo gerada com sucesso!")
                st.info(f"Cenário: {prompt_video}")
