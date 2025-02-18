__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import google.generativeai as genai
import streamlit as st
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from etapas.corretor import planej_campanhas
from etapas.resumidor import resumidor
from etapas.alinhador_jornal import alinhar_jornal
from etapas.alinhador_rede import alinhar
from etapas.resum_entrevista import resumidor_entrevista


st.set_page_config(
    layout="wide",
    page_title="Macfor BetterDoc",
    page_icon="static/page-icon.png"
)

st.image('static/macLogo.png', width=300)
st.text(
        "Empoderada por IA, a Macfor conta com um sistema limpador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e altere documentos de forma automática para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
    )

# Configuração das chaves de API
gemini_api_key = os.getenv("GEM_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

# Inicializa o cliente Tavily
client = TavilyClient(api_key=t_api_key1)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

# Configura o modelo de AI Gemini
genai.configure(api_key=gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")

# Função de login
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.subheader("Página de Login")

    nome_usuario = st.text_input("Nome de Usuário", type="default")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if nome_usuario == "admin" and senha == "senha1234":
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False
    return False

# Função para exibir subseções com explicações
def exibir_subsecoes(selecao_sidebar):

    if selecao_sidebar == "Holambra":
        st.header("Holambra")
        st.text("Utilidades de correção/redação customizadas para as necessidades da Cooperativa Holambra.")
        st.subheader("1. Corretor")
        st.text("Corrija o seu texto de acordo com as normas gramática/ortográficas padrão brasileiras mantendo o sentido principal.")
        st.subheader("2. Resumidor")
        st.text("Resuma o seu texto mantendo o sentido principal.")
        st.subheader("3. Alinhador")
        st.text("Alinhe o seu texto de acordo com o tom de voz da Cooperativa Holambra.")

    elif selecao_sidebar == "Documentos Salvos":
        st.header("Documentos Salvos")
        st.text("Aqui você pode visualizar, editar e organizar todos os documentos gerados ao longo do processo. "
                "Essa área é essencial para manter o controle de todas as estratégias e materiais criados, facilitando o acesso e a edição desses conteúdos quando necessário.")

# Verifique se o login foi feito antes de exibir o conteúdo
if login():
    # Sidebar para escolher entre "Pesquisa e Estratégia", "Cliente", "Midias/Redes" e "Documentos Salvos"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        [

            "Holambra",

        ],
        index=0  # Predefinir como 'Pesquisa e Estratégia' ativo
    )

    # Exibir as subseções com explicações dependendo da seleção no sidebar
    exibir_subsecoes(selecao_sidebar)





    # Seção para "Midias/Redes"
    if selecao_sidebar == "Holambra":
        st.sidebar.subheader("Mídias")
        midias_option = st.sidebar.selectbox(
            "Escolha o tipo de conteúdo Mídias:",
            [

                "Corretor de texto",
                "Resumidor de texto",
                "Alinhador Redes Sociais e Materiais Impressos",
                "Alinhador Jornal Conecta",
                "Resumidor de entrevista"

            ]
        )

        if midias_option != "Selecione uma opção":
            if midias_option == "Corretor de texto":
                planej_campanhas()
            elif midias_option == "Resumidor de texto":
                resumidor()
            elif midias_option == "Alinhador Redes Sociais e Materiais Impressos":
                alinhar()
            elif midias_option == "Alinhador Jornal Conecta":
                alinhar_jornal()
            elif midias_option == "Resumidor de entrevista":
                resumidor_entrevista()


 
