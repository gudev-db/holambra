import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa os modelos do Gemini
modelo_vision = genai.GenerativeModel("gemini-1.5-vision")  # Modelo para imagens
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")  # Modelo para texto

# Guias do cliente
guias = """
Sempre fazer:
- Manter um tom autêntico, educativo, empático e inspirador.
- Reforçar os pilares confiança, qualidade e segurança.
- Seguir as regras ortográficas e gramaticais da Língua Portuguesa.
- Escrever “Loja de Suprimentos” com iniciais maiúsculas.
- A palavra “Cooperativa” sempre com inicial maiúscula.
- Em nomes de regiões, utilizar inicial maiúscula (ex: Sul, Norte).
- Usar primeira pessoa do plural: “Nós somos”, “nós temos”, etc.
- Preferir “CEO” em vez de Presidente Executivo; utilizar “e” minúsculo em “e-Coop”.
- Em materiais impressos, justificar o texto à esquerda.

Sempre evitar:
- Utilizar a palavra “prosperidade” e a hashtag #culturadequalidade.
- Utilizar fotos que mostrem as unidades em páginas seguidas.
- Usar um tom de voz que não seja genuíno ou que não ressoe com os valores da marca.
- Apenas “copiar e colar” informações para os materiais impressos.
"""

# Função para analisar a imagem
def alinhar_img():
    st.subheader('Análise de Imagem')

    # Upload da imagem
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Exibe a imagem carregada
        image = Image.open(uploaded_file)
        st.image(image, caption='Imagem Carregada', use_column_width=True)

        # Converte a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_bytes = img_byte_arr.getvalue()

        # Define o tipo MIME correto
        mime_type = "image/png" if image.format == "PNG" else "image/jpeg"

        # Gera a descrição da imagem usando o Gemini
        with st.spinner('Analisando a imagem...'):
            resposta = modelo_vision.generate_content([
                {"mime_type": mime_type, "data": img_bytes}
            ])
            descricao = resposta.text  # Extraindo a resposta corretamente

        # Exibe a descrição gerada
        st.subheader('Descrição da Imagem')
        st.write(descricao)

        # Prompt para verificar alinhamento com os guias do cliente
        prompt_verificacao = f"""
        Esta é a descrição da imagem fornecida: {descricao}.
        De acordo com os seguintes guias do cliente:
        {guias}
        A imagem está aprovada? Justifique sua resposta.
        """

        # Gera a resposta de verificação usando o modelo de linguagem
        with st.spinner('Verificando alinhamento com os guias do cliente...'):
            resposta_verificacao = modelo_texto.generate_content(prompt_verificacao)
            avaliacao = resposta_verificacao.text  # Extraindo a resposta corretamente

        # Exibe a avaliação
        st.subheader('Avaliação da Imagem')
        st.write(avaliacao)
