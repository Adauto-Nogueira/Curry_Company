
# Libraries 
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# Biblioteca necessária
import pandas as pd
import streamlit as st
from PIL import Image 
import folium
from streamlit_folium import folium_static
import datetime

st.set_page_config(page_title='Visão Entregador', page_icon='🚚', layout='wide' )

#--------------------------------
# Funções
#--------------------------------


def avg_std_per_traffic(df1):
            df_avg_std_per_traffic = (df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                         .groupby('Road_traffic_density')
                                         .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            df_avg_std_per_traffic.columns = ['Dpr_mean','Dpr_std']
            df_avg_std_per_traffic = df_avg_std_per_traffic.reset_index()
            
            return df_avg_std_per_traffic




def top_deliver(df1, top_asc):
            df2 = (df1.loc[:,['Time_taken(min)','City','Delivery_person_ID']]
                 .groupby(['City','Delivery_person_ID'])
                 .min()
                 .sort_values(['City','Time_taken(min)'], ascending=top_asc)
                 .reset_index())

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    
            df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index(drop=True)
        
            return df3
            
    

            
        
def clean_code( df ):
    df.loc[: ,'ID'] = df.loc[:, 'ID'].str.strip()
    df.loc[: ,'Delivery_person_ID'] = df.loc[: ,'Delivery_person_ID'].str.strip()
    df.loc[: ,'Time_Orderd'] = df.loc[: ,'Time_Orderd'].str.strip()
    df.loc[: ,'Type_of_vehicle'] = df.loc[: ,'Type_of_vehicle'].str.strip()
    df.loc[: ,'City'] = df.loc[: ,'City'].str.strip()
    df.loc[: ,'Road_traffic_density'] = df.loc[: ,'Road_traffic_density'].str.strip()
    
    # Excluir as linhas com idades dos entregadores vazia
    # (conceito de seleção condicional)
    linhas_vazias = (df['Delivery_person_ID'] != 'NaN') & (df['City'] != 'NaN') & (df['Road_traffic_density'] != 'NaN ') & (df['Delivery_person_Age'] != 'NaN ') & (df['multiple_deliveries'] != 'NaN ') & (df['Festival'] != 'NaN ')
    
    df = df.loc[linhas_vazias, :]

    # Conversão de texto/categorias/strigs para inteiros
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)
    
    # Conversão de texto/categoria/strings para numeros decimais
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)
    
    # Conversão de texto para data
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
    
    # Conversão de texto para int
    df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)
    
    # Tirando texto de números
    
    df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
    
    return df



# Importar dataset
df = pd.read_csv('train.csv')

# Limpeza de dados

df1 = clean_code( df )


# =======================================
# Barra Lateral
# =======================================

st.header('Marketplace - Visão entregador')

#image_path = 'C:\\Users\\adaut_gg\\repos_cds\\FTC\\Ciclo_6_Conceito_de_ETL\\logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=300)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fast Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual o valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 3, 19),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['High', 'Jam', 'Low', 'Medium'],
    default='Low' )

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#------------------------- Início da estrutura lógica do código ----------- 


# =======================================
# Layout Streamlit
# =======================================


tab1,tab2,tab3 = st.tabs(['Visão gerencial','_','_'])

with tab1:
    st.header('Overall ratings')
    with st.container():
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)
        
        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)
            
        with col4: 
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)
            
st.markdown('''---''')

st.header('Avaliação')
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('##### Avaliação média por entregador')
        
        df_avg_rating_per_deliver = (df1.loc[:, ['Delivery_person_Ratings','Delivery_person_ID']]
                    .groupby('Delivery_person_ID')
                    .mean()
                    .reset_index())
        
        st.dataframe(df_avg_rating_per_deliver)
        
        
        
    with col2:
        st.markdown('##### Avaliação média e desvio padrão por trânsito')
        df_avg_std_per_traffic = avg_std_per_traffic(df1)
        st.dataframe( df_avg_std_per_traffic )
        
        
        
        
        st.markdown('##### Avaliação média e desvio padrão por condição climática')
        df_avg_std_per_weather = (df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
                     .groupby('Weatherconditions')
                     .agg({'Delivery_person_Ratings': ['mean', 'std']}))

        df_avg_std_per_weather.columns = ['Dpr_mean','Dpr_std']
        df_avg_std_per_weather = df_avg_std_per_weather.reset_index()
        st.dataframe(df_avg_std_per_weather)
            
            
st.markdown('''---''')

st.header('Velocidade de entrega')
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('##### Top entregadores mais rápidos')
        df3 = top_deliver(df1, top_asc=True)
        st.dataframe(df3)
        
        
    with col2:
        st.markdown('##### Top entregadores mais lentos')
        df3 = top_deliver(df1, top_asc=False)
        st.dataframe(df3)
        
        
        
            
            
            






