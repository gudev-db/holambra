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
-Manter um tom autêntico, educativo, empático e inspirador.
-Reforçar os pilares confiança, qualidade e segurança. Também é
importante destacar a estrutura da Cooperativa para atender os
clientes.
-Seguir as regras ortográficas e gramaticais da Língua
Portuguesa.
-Escrever “Loja de Suprimentos”, como título, sempre com as duas
palavras em inicial caixa-alta
-A palavra “Cooperativa”, quando se refere à Holambra, sempre
se escreve com inicial maiúscula.
-Em nome de regiões “Sul, Norte” utilizar inicial maiúscula.
-Dar preferência ao uso da primeira pessoa do plural = “Nós
somos”, “nós temos”, “fazemos”, “nosso compromisso”. Não usar
terceira pessoa do singular para se referir à marca.
-Preferir “CEO”, em vez de Presidente Executivo; utilizar “e”
minúsculo em “e-Coop”.
-Em materiais impressos justificar o texto à esquerda
'''


donts = '''

Sempre evitar:
-Utilizar a palavra “prosperidade” e a hashtag #culturade
qualidade
-Utilizar fotos que mostrem as unidades em páginas
seguidas.
-Usar um tom de voz que não seja genuíno ou que não
ressoe com os valores da marca.
-Apenas “copiar e colar” informações para os materiais
impressos. Os dados originais devem estar lá, mas
adaptados para uma linguagem mais atrativa e simples
para o cooperado.
'''



# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def alinhar():
    st.subheader('Redes sociais e materiais impressos')

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
                  
                        
                        
                        
                    - Corrija-o se atentando aos padrões ortográficos e gramaticais da língua portuguesa brasileira de uma forma que mantenha o sentido do texto.
                        """
                    corrected_output = modelo_linguagem.generate_content(prompt_texto).text

                     


                        # Exibe os resultados na interface
                    st.header('Texto alinhado')
                    st.markdown(corrected_output)
                  


