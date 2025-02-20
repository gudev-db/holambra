import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o cliente Gemini
client = genai.Client(api_key=gemini_api_key)

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

        # Gera a descrição da imagem usando o modelo "gemini-2.0-flash"
        with st.spinner('Analisando a imagem...'):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["What is this image?", img_bytes]
            )
            descricao = response.text  # Extraindo a resposta corretamente

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

        # Gera a resposta de verificação usando o modelo de linguagem "gemini-1.5-flash"
        with st.spinner('Verificando alinhamento com os guias do cliente...'):
            response_verificacao = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt_verificacao]
            )
            avaliacao = response_verificacao.text  # Extraindo a resposta corretamente

        # Exibe a avaliação
        st.subheader('Avaliação da Imagem')
        st.write(avaliacao)
