__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from etapas.corretor import planej_campanhas


st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="static/page-icon.png"
)

st.image('static/macLogo.png', width=300)
st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
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
    if selecao_sidebar == "Planejamento":
        st.header("Planejamento")
        st.text("Desenvolva estratégias sólidas com base em pesquisa detalhada e em tendências do mercado.")
        st.subheader("1. Planejamento de Pesquisa e Estratégia")
        st.text("Desenvolva um planejamento tático e de pesquisa robusto que guiará todas as ações estratégicas de marketing da sua empresa.")
        st.subheader("2. Pesquisa de Tendências")
        st.text("Acompanhe as últimas tendências do mercado, ajudando a guiar suas decisões de marketing e garantindo que sua empresa esteja à frente.")

    elif selecao_sidebar == "CRM":
        st.header("CRM")
        st.text("Desenvolva estratégias focadas no relacionamento com seus clientes e na comunicação personalizada.")
        st.subheader("1. Automação de Marketing")
        st.text("Construa um fluxo de comunicação eficaz com seus leads e clientes. Estruture estratégias de relacionamento, automação de processos e gestão de dados.")
        st.subheader("2. Cronograma de Temas de Emails")
        st.text("Planeje campanhas de email marketing com um cronograma estratégico, criando uma jornada de comunicação eficiente com seus leads.")
        st.subheader("3. Redação de Emails")
        st.text("Gere exemplos de emails com base nas melhores práticas de comunicação para aumentar a eficácia da comunicação com seus leads.")
        st.subheader("4. Investigação de Leads")
        st.text("Aprofunde-se no perfil do seu lead e obtenha informações detalhadas sobre suas necessidades e comportamentos.")

    elif selecao_sidebar == "Mídias":
        st.header("Mídias")
        st.text("Elabore e otimize estratégias para a gestão de mídias sociais e criação de conteúdo visual impactante.")
        st.subheader("1. Planejamento de Mídias e Redes")
        st.text("Crie um planejamento detalhado para sua gestão de mídias e redes sociais. Com esse plano, você poderá traçar estratégias criativas para atrair, engajar e fidelizar seu público.")
        st.subheader("2. Brainstorming de Anúncios")
        st.text("Alavanque suas campanhas publicitárias com um brainstorming detalhado para anúncios. Gere várias sugestões criativas para engajar e converter seu público.")
        st.subheader("3. Geração de Imagens")
        st.text("Dê vida ao seu conteúdo visual com ideias de imagens geradas com base em uma descrição detalhada do que deseja comunicar.")

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

            "Mídias",

        ],
        index=0  # Predefinir como 'Pesquisa e Estratégia' ativo
    )

    # Exibir as subseções com explicações dependendo da seleção no sidebar
    exibir_subsecoes(selecao_sidebar)





    # Seção para "Midias/Redes"
    if selecao_sidebar == "Mídias":
        st.sidebar.subheader("Mídias")
        midias_option = st.sidebar.selectbox(
            "Escolha o tipo de conteúdo Mídias:",
            [

                "Brainstorming de Anúncios",

            ]
        )

        if midias_option != "Selecione uma opção":
            if midias_option == "Brainstorming de Anúncios":
                planej_campanhas()


 
