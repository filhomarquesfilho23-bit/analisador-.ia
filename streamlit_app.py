
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import time
​Configuração da página Streamlit
​st.set_page_config(
page_title="ObraSmart - Assistente de Engenharia Civil",
page_icon="🏗️",
layout="wide"
)
​st.title("🏗️ ObraSmart - Inteligência Artificial para Engenharia Civil")
st.markdown("Plataforma comercial avançada para engenharia estrutural, orçamentação e visualização multimédia.")
​Painel Lateral para Configurações e Módulos
​with st.sidebar:
st.header("⚙️ Configurações da Aplicação")
api_key = st.text_input("Insira sua chave API do Google Gemini", type="password")
​selected_model = st.selectbox(
"Escolha o modelo de IA",
["gemini-2.5-flash", "gemini-2.5-pro"]
)
​st.markdown("---")
st.markdown("### Módulos do ObraSmart")
modulo = st.radio(
"Selecione a ferramenta:",
[
"Chat Técnico & Normas (Multimodal)",
"Gerador de Renders (Imagens)",
"Simulador de Canteiro (Vídeos)"
]
)
​st.markdown("---")
st.markdown("### Modelo Comercial (SaaS)")
st.info("Licença B2B Ativa • ObraSmart Cloud")
​Validação da Chave de API
​if not api_key:
st.warning("⚠️ Por favor, insira a sua chave API do Google Gemini no painel lateral para desbloquear o sistema.")
st.stop()
​Inicializar o cliente oficial da API Google GenAI
​client = genai.Client(api_key=api_key)
​---------------------------------------------------------
​MÓDULO 1: CHAT TÉCNICO & ANÁLISE DE PROJETOS (MULTIMODAL)
​---------------------------------------------------------
​if modulo == "Chat Técnico & Normas (Multimodal)":
st.subheader("💬 Consultoria Estrutural e Análise de Documentos")
st.markdown("Faça perguntas técnicas, cálculos preliminares ou carregue plantas, PDFs e imagens de obra.")
​# System Instruction com a Persona de Engenheiro Civil Sénior e Disclaimer Obrigatório
system_instruction = (
"És o ObraSmart, um Engenheiro Civil Sénior altamente especializado em análise estrutural, "
"materiais de construção, fundações e conformidade com normas técnicas (Eurocódigos e ABNT). "
"Fornece respostas rigorosas, profissionais, estruturadas e passo a passo. "
"IMPORTANTE: Termina obrigatoriamente todas as respostas com um aviso legal claro a relembrar "
"que esta análise serve exclusivamente como apoio técnico preliminar e deve ser obrigatoriamente "
"revista, validada e assinada por um engenheiro civil devidamente habilitado e responsável pelo projeto."
)
​pergunta_utilizador = st.text_area(
"Descreva a questão de engenharia ou os parâmetros estruturais:",
placeholder="Ex: Como proceder ao cálculo de armadura longitudinal para uma viga contínua com 8 metros de vão?"
)
​ficheiro_carregado = st.file_uploader(
"Carregar ficheiro técnico (Imagem, PDF, TXT ou CSV)",
type=["png", "jpg", "jpeg", "pdf", "txt", "csv"]
)
​if st.button("Executar Análise Técnica", type="primary"):
if not pergunta_utilizador and not ficheiro_carregado:
st.error("Por favor, insira uma pergunta ou carregue um ficheiro técnico.")
else:
with st.spinner("O ObraSmart está a processar os dados técnicos e normativos..."):
try:
conteudos = []
​# Processar upload se existir
if ficheiro_carregado:
file_bytes = ficheiro_carregado.read()
mime_type = ficheiro_carregado.type
​# Se for imagem, usar Image do PIL para envio inline seguro
if "image" in mime_type:
img = Image.open(io.BytesIO(file_bytes))
conteudos.append(img)
else:
# Para outros ficheiros, enviar como bytes usando types.Part
part_file = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
conteudos.append(part_file)
​if pergunta_utilizador:
conteudos.append(pergunta_utilizador)
​# Configurar e chamar o modelo Gemini
config = types.GenerateContentConfig(
system_instruction=system_instruction,
temperature=0.2
)
​response = client.models.generate_content(
model=selected_model,
contents=conteudos,
config=config
)
​st.markdown("### 📊 Relatório Técnico do ObraSmart:")
st.write(response.text)
​except Exception as e:
st.error(f"Ocorreu um erro ao comunicar com a API: {e}")
​---------------------------------------------------------
​MÓDULO 2: GERADOR DE RENDERS E VISUALIZAÇÃO (IMAGEM)
​---------------------------------------------------------
​elif modulo == "Gerador de Renders (Imagens)":
st.subheader("🎨 Geração de Renders Fotorrealistas")
st.markdown("Crie imagens conceituais de fachadas, interiores ou pormenores construtivos a partir de texto.")
​prompt_imagem = st.text_input(
"Descrição detalhada do render desejado:",
placeholder="Ex: Render fotorrealista de uma estrutura metálica e vidro em edifício comercial, iluminação natural diurna."
)
​aspecto_img = st.selectbox("Proporção da Imagem:", ["1:1", "16:9", "9:16", "4:3"])
​if st.button("Gerar Render do Projeto", type="primary"):
if not prompt_imagem:
st.error("Por favor, introduza uma descrição para gerar o render.")
else:
with st.spinner("A gerar render fotorrealista através do modelo visual..."):
try:
# Chamada ao modelo de imagem avançado
image_response = client.models.generate_content(
model='gemini-2.5-flash-image',
contents=[prompt_imagem],
config=types.GenerateContentConfig(
response_modalities=["IMAGE"],
image_config=types.ImageConfig(aspect_ratio=aspecto_img)
)
)
​# Procurar partes de imagem na resposta
imagem_encontrada = False
for part in image_response.parts:
if part.inline_data:
image_bytes = part.inline_data.data
img_obj = Image.open(io.BytesIO(image_bytes))
st.image(img_obj, caption=f"Render: {prompt_imagem}", use_container_width=True)
imagem_encontrada = True
​if not imagem_encontrada:
st.warning("O modelo não retornou uma imagem direta. Tente ajustar a descrição.")
​except Exception as e:
st.error(f"Erro ao gerar a imagem: {e}. Certifique-se de que a sua chave suporta o modelo de imagem.")
​---------------------------------------------------------
​MÓDULO 3: SIMULADOR DE CANTEIRO DE OBRAS (VÍDEOS)
​---------------------------------------------------------
​elif modulo == "Simulador de Canteiro (Vídeos)":
st.subheader("🎥 Simulações Dinâmicas e Vídeos de Canteiro")
st.markdown("Gere simulações em vídeo para planeamento logístico ou apresentações comerciais a clientes.")
​prompt_video = st.text_input(
"Descrição da simulação em vídeo:",
placeholder="Ex: Timelapse fotorrealista da betonagem de uma laje de fundação num canteiro urbano."
)
​aspecto_video = st.selectbox("Formato do Vídeo:", ["16:9 (Paisagem)", "9:16 (Retrato)"])
​if st.button("Gerar Simulação em Vídeo", type="primary"):
if not prompt_video:
st.error("Por favor, introduza uma descrição para o vídeo.")
else:
with st.spinner("A iniciar o processo de geração de vídeo (Veo)... Isto poderá demorar alguns momentos."):
try:
# Configuração para geração de vídeo utilizando o modelo Veo
ratio_val = "16:9" if "16:9" in aspecto_video else "9:16"
​operation = client.models.generate_videos(
model='veo-3.1-generate-preview',
prompt=prompt_video,
config=types.GenerateVideosConfig(
aspect_ratio=ratio_val
)
)
​st.info("Operação de vídeo iniciada na nuvem. A aguardar conclusão...")
​# Fazer polling da operação até estar concluída
progress_bar = st.progress(0)
attempts = 0
while not operation.done and attempts < 60:
time.sleep(5)
attempts += 1
progress_bar.progress(min(attempts * 2, 100))
​if operation.done:
st.success("Simulação em vídeo gerada com sucesso!")
st.write("O vídeo está pronto para exportação e apresentação comercial.")
else:
st.warning("A geração demorou mais do que o esperado. Verifique o painel do AI Studio.")
​except Exception as e:
st.error(f"O modelo de vídeo requer permissões específicas na API. Erro: {e}")
