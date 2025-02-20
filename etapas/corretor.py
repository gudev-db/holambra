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






# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def planej_campanhas():
    st.subheader('Corretor de texto')

    texto = st.text_area('Texto a ser analisado:', help="Digite/Cole aqui o texto a ser analisado", height = 300)
   

    if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
        st.subheader("Anúncio gerado")
        for tarefa in st.session_state.resultados_tarefas:
            st.markdown(f"**Arquivo**: {tarefa['output_file']}")
            st.markdown(tarefa["output"])
        
        if st.button("Gerar Novo Anúncio"):
            limpar_estado()
            st.experimental_rerun()
    else:
        if st.button('Corrigir'):
            if 1 ==1:
                with st.spinner('Corrigindo...'):
                    prompt_texto = f"""
                    Dado o texto: {texto};
                  
                        
                        
                        
                    - Corrija-o se atentando aos padrões ortográficos e gramaticais da língua portuguesa brasileira de uma forma que mantenha o sentido do texto. Não resuma. Me traga o texto inteiro correto.
                    - crie comentários abaixo sobre o que foi alterado no texto   """
                    corrected_output = modelo_linguagem.generate_content(prompt_texto).text

                     


                        # Exibe os resultados na interface
                    st.header('Texto corrigido')
                    st.markdown(corrected_output)
                  



