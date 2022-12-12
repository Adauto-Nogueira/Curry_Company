import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='👽'
)

#image_path = 'C:\\Users\\adaut_gg\\repos_cds\\FTC\\Ciclo_6_Conceito_de_ETL\\logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=300)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fast Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
""" Growth Dashboard foi construído para acompanhar as métricas de  crescimento da Empresa, Entregadores e Restaurante.
    ### Como utilizar esse Groth Dashboard?
    - Visão Empresa:
        - Visão gerencial: Métricas gerais de comportamento.
        - Visão tática: Indicadores semanais de crescimento
        - Visão geográfica: Insights de geolocalização
    - Visão Entregadores:
        - Acompanhamento de indicadores semanais de crescimento
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
        
    ### Ask for Help
    - Time de Data Science no Discord:
        Adauto Nogueira#1198

""")

