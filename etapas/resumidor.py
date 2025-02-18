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


guias_marca = '''

Guia completo para criar um mote de campanha eficaz

Você já se perguntou como algumas campanhas publicitárias conseguem capturar a atenção do público e se tornar um sucesso instantâneo? A resposta está, muitas vezes, no poder de um mote de campanha eficaz.
Um mote de campanha é uma frase ou slogan curto e memorável que representa a essência da mensagem que uma empresa ou organização deseja transmitir ao público. É a oportunidade de criar uma conexão emocional com os consumidores e despertar interesse em relação ao produto ou serviço oferecido.
Para criar um mote de campanha eficaz, é importante levar em consideração alguns elementos-chave:
Clareza: O mote deve transmitir a mensagem de forma direta e compreensível. Evite termos complexos ou ambíguos que possam confundir o público-alvo.
Emoção: Um bom mote deve despertar emoções no público, seja alegria, curiosidade, surpresa ou qualquer outro sentimento que crie uma conexão emocional com a marca.
Originalidade: É importante criar um mote que seja único e diferenciado dos concorrentes. Isso ajudará a marca a se destacar e a ser lembrada pelos consumidores.
Relevância: O mote deve estar alinhado com os valores e propósitos da marca, além de ser relevante para o público-alvo. Conhecer bem o mercado e o perfil dos consumidores é essencial para criar um mote que ressoe com eles.
Memorabilidade: Um bom mote deve ser fácil de lembrar. Pense em frases curtas, simples e impactantes que fiquem na mente das pessoas por um longo tempo.
É importante ressaltar que a criação de um mote de campanha eficaz requer habilidades de marketing e comunicação. Embora este guia forneça dicas valiosas, ele não substitui a assessoria jurídica especializada. É recomendável que as empresas consultem profissionais qualificados para garantir que o mote esteja em conformidade com as leis e regulamentações vigentes.
Ao criar um mote de campanha, é fundamental realizar pesquisas de mercado, analisar a concorrência e testar diferentes opções com o público-alvo. Aperfeiçoar o mote com base no feedback recebido é uma prática recomendada para garantir sua eficácia.
Em resumo, um mote de campanha eficaz é uma poderosa ferramenta de comunicação que pode impulsionar o sucesso de uma campanha publicitária. Seguir os princípios de clareza, emoção, originalidade, relevância e memorabilidade ajudará a criar um mote que se destaque e conecte com o público-alvo. Lembre-se sempre de buscar a orientação adequada para garantir conformidade legal.

'''



# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def resumidor():
    st.subheader('Resumidor de texto')

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
        if st.button('Iniciar Planejamento'):
            if 1 ==1:
                with st.spinner('Corrigindo...'):
                    prompt_texto = f"""
                    Dado o texto: {texto};
                  
                        
                        
                        
                    - Resuma o texto se atentando aos padrões ortográficos e gramaticais da língua portuguesa brasileira de uma forma que mantenha o sentido do texto.
                        """
                    corrected_output = modelo_linguagem.generate_content(prompt_texto).text

                     


                        # Exibe os resultados na interface
                    st.header('Texto corrigido')
                    st.markdown(corrected_output)
                  


