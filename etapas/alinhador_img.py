import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa os modelos do Gemini
modelo_vision = genai.GenerativeModel("gemini-2.0-flash")  # Modelo para imagens
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")  # Modelo para texto

# Guias do cliente
guias = """

- Cliente quer uma imagem limpa. Sem sujeira
- Cliente não quer pessoas de bermuda
- Cliente não quer 'personificar' a marca. Então fotos com uma única pessoa não podem.
- Imagens devem ser acertivas
- Sem 0 antes dos números
- deixar a fonte mais de rodapé e trabalhar mais o título para chamar mais atenção
- ícone ao lado das culturas para chamar atenção
- em sinal de atenção, colocaria um ícone para ilustrar

"""

# Função para analisar a imagem
def alinhar_img():
    st.subheader('Análise de Imagem')

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

        # Gera a descrição da imagem usando o Gemini
        try:
            with st.spinner('Analisando a imagem...'):
                resposta = modelo_vision.generate_content([
                    {"mime_type": mime_type, "data": img_bytes},
                    {"text": "O que há nessa imagem?"}  # Adiciona um parâmetro de texto vazio
                ])
                descricao = resposta.text  # Extraindo a resposta corretamente
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar a imagem: {e}")
            return

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

        try:
            # Gera a resposta de verificação usando o modelo de linguagem
            with st.spinner('Verificando alinhamento com os guias do cliente...'):
                resposta_verificacao = modelo_texto.generate_content(prompt_verificacao)
                avaliacao = resposta_verificacao.text  # Corrigido o acesso à resposta
        except Exception as e:
            st.error(f"Ocorreu um erro ao verificar a imagem: {e}")
            return

        # Exibe a avaliação
        st.subheader('Avaliação da Imagem')
        st.write(avaliacao)

    # Botão para remover a imagem
    if st.button("Remover Imagem"):
        st.session_state.image = None
        st.experimental_rerun()  # Atualiza a aplicação

    # Se uma imagem foi armazenada no estado da sessão, exibe a opção de remover
    if st.session_state.image is not None:
        st.info("Imagem carregada. Clique no botão acima para removê-la.")
