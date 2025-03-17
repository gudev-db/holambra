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

# Guias do cliente
guias = """

Comment: Usaria ícone ao lado das culturas para chamar atenção
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:25:15.769Z
----
Comment: achei que ficou com muita informação
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:24:09.943Z
----
Comment: Sugiro deixar a fonte mais de rodapé e trabalhar mais o título para chamar mais atenção
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:23:30.036Z
----
Comment: Esse cenário ainda continua com a virada do ano? Vale revisar/atualizar?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:57:47.386Z
----
Comment: Será que vale falar para contarem com a Holambra na venda de sementes, tratamento e monitoramento?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:51:31.840Z
----
Comment: o sol ficou muito estourado, né?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:50:12.319Z
----
Comment: Como é sinal de atenção, colocaria um ícone para ilustrar
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:49:06.850Z
----
Comment: Verificar se o vermelho está correto. Na minha tela pareceu rosa. Além disso, confirmar se é  essa foto que é antiga (sem as atualizações do parque industrial)
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:47:17.778Z
----
Comment: @snjezana.abreu@holambra.com.br, validar com o Pitt. Pelo o que ouvi, ainda não é superior, mas até 400 mil. Talvez: armazenagem de até 400 mil toneladas
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:46:51.473Z
----
Comment: As # precisam ter caixa alta e baixa? É melhor para identificação?

EmCampo, DaSoja...
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:15:12.324Z
----
Comment: não gostei do gerúndio, talvez tirar?

... dessa jornada com soluções cada vez mais eficientes e sustentáveis
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:13:36.641Z
----
Comment: No primeiro evento do ano, realizado em Itaberá-SP, reunimos cooperados, produtores...
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:08:52.726Z
----
Comment: Sugestão: 

🌱Holambra em Campo 2025: conectando tecnologia e inovação na cultura da soja!

 
No primeiro evento do ano, reunimos cooperados, produtores, especialistas e empresas parceiras para compartilhar conhecimento, apresentar tendências e debater as inovações que estão transformando o campo.

Agradecemos a todos que participaram e às empresas que fazem parte dessa jornada, fortalecendo com soluções cada vez mais eficientes e sustentáveis.

🎥 Confira no vídeo os melhores momentos do Holambra em Campo e veja como, juntos, estamos cultivando o futuro da produção agrícola!
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:45:37.150Z
----
Comment: cooperados, produtores, especialistas e empresas parceiras
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:39:27.662Z
----
Comment: Algo mais nese sentido:

Demos início à programação de eventos de 2025 com o primeiro Holambra em Campo do ano, conectando tecnologia e inovação à cultura da soja!
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:38:12.104Z
----
Comment: retirar
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:32:55.861Z
----
Comment: Sugestão:

Parabéns, Santa Cruz do Rio Pardo! 

São 155 anos de história, crescimento e desenvolvimento! Desde julho de 2024, temos a honra de fazer parte com nossa loja, contribuindo para o progresso dos produtores locais e fortalecendo o agronegócio da região.

Queremos seguir ao lado dos nossos clientes santa-cruzenses, apoiando cada nova conquista! 

#HolambraCooperativa #Cooperativa #SantaCruzdoRioPardo
Created by: Snjezana Simunovic
Created at: 2025-01-20T17:50:04.526Z
----
Comment: Gosto mais dessa opção, mas não vejo qual a relevância dessa infermoção para o nosso negócio, não temos produtores de arroz.

Conforme combinado, nos aniversários das cidades, utilizaremos uma foto da cidade junto com a da loja ou unidade correspondente.
Created by: Snjezana Simunovic
Created at: 2025-01-20T14:34:08.755Z
----
comments_2025-02-27T11:12:29.725Z.txt
Displaying comments_2025-02-27T11:12:29.725Z.txt.
"""

# Função para analisar a imagem
def alinhar_img():
    st.subheader('Aprovação de Criativos')

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

        # Prompt para analisar a imagem
        #prompt = "Descreva em máximo e profundo e extremo detalhe tudo que está contido nessa imagem (o seu retorno será toda a referência que o próximo prompt terá como referência sobre o que está na imagem, então, não deixe nada passar). Desde uma descrição extremamente detalhada da imagem, até os textos, elementos gráficos e cores mais prominentes contidas nela se os existirem. Diga se o sol (se presente) brilha demais ao ponto de ofuscar demais a imagem."
        prompt = f'''

        Você está aqui para aprovar imagens de criativos para campanhas de marketing digital para a cooperativa holambra. 
        Se atente ao mínimo e extremo detalhe de tudo que está na imagem, você é uma pessoa extrema e profundamente detalhista.
        
        O cliente Holambra já deu alguns feedbacks sobre criativos no passado, como detalhados em {guias}.
        
        

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

        # # Prompt para verificar alinhamento com os guias do cliente
        # prompt_verificacao = f"""
        # Esta é a descrição da imagem fornecida: {descricao}.
        # De acordo com os seguintes guias do cliente:
        # {guias}
        # A imagem está aprovada? Justifique sua resposta.
        # """

        # try:
        #     # Gera a resposta de verificação usando o modelo de linguagem
        #     with st.spinner('Verificando alinhamento com os guias do cliente...'):
        #         resposta_verificacao = modelo_texto.generate_content(prompt_verificacao)
        #         avaliacao = resposta_verificacao.text  # Corrigido o acesso à resposta
        # except Exception as e:
        #     st.error(f"Ocorreu um erro ao verificar a imagem: {e}")
        #     return

        # Exibe a avaliação
        #st.subheader('Avaliação da Imagem')
        #st.write(avaliacao)

    # Botão para remover a imagem
    if st.button("Remover Imagem"):
        st.session_state.image = None
        st.experimental_rerun()  # Atualiza a aplicação

    # Se uma imagem foi armazenada no estado da sessão, exibe a opção de remover
    if st.session_state.image is not None:
        st.info("Imagem carregada. Clique no botão acima para removê-la.")
