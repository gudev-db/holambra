import streamlit as st
import google.generativeai as genai
import uuid
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini



# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())


dos = '''

Sempre fazer:
- O objetivo do projeto é informar nosso público cooperado sobre
as últimas notícias e eventos relevantes da Cooperativa. Cada
notícia deve informar sobre o tema: o quê, quando, onde, como e
porque aconteceu.
- As notícias devem ser redigidas com objetividade e simplicidade,
na 3º pessoa do singular.
- O tom de voz deve ser formal. Nosso público é exigente,
detalhista e conservador, preferindo textos muito bem escritos.
Seguir as regras ortográficas e gramaticais da Língua
Portuguesa.
- A palavra “Cooperativa”, quando se refere à Holambra, sempre
se escreve com inicial maiúscula.
- Em nome de regiões “Região Sul, Norte” utilizar inicial maiúscula.
- Em toda matéria, deve haver fotos, com legendas nessas fotos, e
indicação da fonte para a matéria, seja o entrevistado ou
Departamento ao qual pertecence.
- Justificar o texto à esquerda.
'''


donts = '''
Sempre evitar:
- Repetições de texto e palavras.
- Nomes das fontes escritos errados.
- Ultrapassar as 12 páginas do informativo.
- Parágrafos e blocos de texto colados um ao outro.
- Textos e boxes desalinhados, e elementos cortando o
texto.
- Ponto final nos textos de legenda das fotos,
jornalisticamente é incorreto.
- Viúvas no texto.
- Fotos que ocupam grande parte da página.
'''



# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def alinhar_jornal():
    st.subheader('Jornal Conecta')

    texto = st.text_area('Texto a ser alinhado:', help="Digite/Cole aqui o texto a ser analisado", height = 300)
   

    if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
        st.subheader("Anúncio gerado")
        for tarefa in st.session_state.resultados_tarefas:
            st.markdown(f"**Arquivo**: {tarefa['output_file']}")
            st.markdown(tarefa["output"])
        
        if st.button("Gerar Novo Anúncio"):
            limpar_estado()
            st.experimental_rerun()
    else:
        if st.button('Alinhar'):
            if 1 ==1:
                with st.spinner('Alinhando...'):
                    prompt_texto = f"""
                    Dado o texto: {texto};
                  
                        
                        
                        
                    - Corrija-o se atentando aos

                    
                    - Do's: {dos};
                    - Don'ts {donts};

                    
                        """
                    corrected_output = modelo_linguagem.generate_content(prompt_texto).text

                     


                        # Exibe os resultados na interface
                    st.header('Texto alinhado')
                    st.markdown(corrected_output)
                  

