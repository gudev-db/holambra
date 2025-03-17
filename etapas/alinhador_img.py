import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa os modelos do Gemini
modelo_vision = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={
        "temperature": 0.1  # Ajuste a temperatura aqui
    }
)  # Modelo para imagens
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")  # Modelo para texto

# Guias do cliente (exemplo)
guias = """
Comente sobre os detalhes da imagem, como cores, fontes, etc.
"""

# Função para analisar a imagem
def alinhar_img():
    st.subheader('Aprovação de Criativos')

    # Campo para o usuário inserir diretrizes personalizadas de aprovação
    diretrizes_aprovacao = st.text_area("Adicione diretrizes de aprovação (opcional)", 
                                        value="")

    # Criação de um estado para controlar a imagem carregada
    if 'image' not in st.session_state:
        st.session_state.image = None

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

        # Armazena a imagem no estado da sessão
        st.session_state.image = image

        # Prompt para analisar a imagem com base nas diretrizes fornecidas
        prompt = f'''
        Você está aqui para aprovar imagens de criativos para campanhas de marketing digital para a cooperativa holambra. 
        Se atente ao mínimo e extremo detalhe de tudo que está na imagem, você é uma pessoa extrema e profundamente detalhista.
        
        O cliente Holambra já deu alguns feedbacks sobre criativos no passado, como detalhados em {guias}.
        
        Diretrizes adicionais fornecidas pelo usuário: {diretrizes_aprovacao}.
        
        Com base nos requisitos de aprovação, diga se a imagem está aprovada ou não.
        '''

        # Gera a descrição da imagem usando o Gemini
        try:
            with st.spinner('Analisando a imagem...'):
                resposta = modelo_vision.generate_content(
                    contents=[prompt, {"mime_type": mime_type, "data": img_bytes}]
                )
                descricao = resposta.text  # Extraindo a resposta corretamente
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar a imagem: {e}")
            return

        # Exibe a descrição gerada
        st.subheader('Aprovação da Imagem')
        st.write(descricao)

    # Botão para remover a imagem
    if st.button("Remover Imagem"):
        st.session_state.image = None
        st.experimental_rerun()  # Atualiza a aplicação

    # Se uma imagem foi armazenada no estado da sessão, exibe a opção de remover
    if st.session_state.image is not None:
        st.info("Imagem carregada. Clique no botão acima para removê-la.")
