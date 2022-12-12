
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

st.set_page_config(page_title='Visão Empresa', page_icon='📈', layout='wide' )

# Importar dataset
df = pd.read_csv('train.csv')

#------------------------
#  Funções
#------------------------


def country_maps(df1):
        df_aux = (df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'City', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())
    
        df_aux = df_aux.head(30)
    
        map = folium.Map()
    
        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'],
                   location_info['Delivery_location_longitude' ]], popup=location_info[['City', 'Road_traffic_density']] ).add_to(map)
    
        folium_static(map, width=1024, height=600 )
        
        


def order_share_by_week(df1):
            df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
            df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
            df_aux = pd.merge(df_aux1, df_aux2, how='inner')
            
            df_aux['Order_by_Delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
            fig = px.line(df_aux, x='week_of_year', y='Order_by_Delivery')
            
            return fig


def order_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
        
    pedido_sem = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        
    fig = px.line(pedido_sem, x='week_of_year', y='ID')
    
    return fig
        

def order_metric(df1):
    pedidos_dia = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
        
    fig = px.bar(pedidos_dia, x='Order_Date', y='ID')
        
    return fig



def traffic_order_city(df1):
            H = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            
            fig = px.scatter(H, x='City', y='Road_traffic_density', size='ID' )
            
            return fig


def order_traffic_share(df1):
    pedido_trafego = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            
    pedido_trafego['ped_tra'] = 100 * (pedido_trafego['ID'] / pedido_trafego['ID'].sum())
            
    fig = px.pie(pedido_trafego, values='ped_tra', names='Road_traffic_density')
            
    return fig


def clean_code( df ):
    """ Está função tem a responsabilidade de limpar o dataset
    1. Remoção dos espaços das strings
    2. Excluir linhas com valores 'NaN'
    3. Mudança do tipo de dado das colunas
    4. Formatação da coluna de data
    5. Limpeza da coluna tempo (remoção do texto, da variável numérica)
    
    Input: Dataframe (df1)
    Output: Dataframe (df1)
    """
    

    # Remover espaços das strings
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

#============================= Início da estrutura Lógica do código ==================

# Limpeza de dados

df1 = clean_code( df )


# Visão empresa

# =======================================
# Barra Lateral
# =======================================

st.header('Marketplace - Visão Cliente')

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
    min_value=pd.datetime(2022, 3, 1),
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

# =======================================
# Layout Streamlit
# =======================================

tab1,tab2,tab3 = st.tabs(['Visão gerencial','Visão tática','Visão geográfica'])

with tab1:
    with st.container():
        st.markdown('# Orders by day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('## Pedidos por tráfego')
            fig = order_traffic_share(df1)
            st.plotly_chart(fig, use_container_width=True) 
            
            
        with col2:
            
            st.markdown('## Volume de pedidos por cidade e tráfego')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)                       
            
            
            
            
with tab2:
    with st.container():
        st.markdown('## Quantidade de pedidos por semana')
        fig = order_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    with st.container():
        st.markdown('## Pedidos por entregador e por semana')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
        
            
                    
            
with tab3:
    st.header('Mapa do país')
    country_maps(df1)
    
       
    
print('Estou aqui')