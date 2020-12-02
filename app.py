import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import plotly.express as px
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from PIL import Image
ALPHAVANTAGE_API_KEY = 'H983JJABQU6EEV35'
ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
cc = CryptoCurrencies(key=ALPHAVANTAGE_API_KEY, output_format='pandas')

resp = requests.get('https://www.alphavantage.co/query', params={
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': 'BTOW3.SA',
    'market': 'BRL',
    'apikey': ALPHAVANTAGE_API_KEY,
    'datatype': 'json',
    'outputsize': "full"})
doc = resp.json()
        
df = pd.DataFrame.from_dict(doc['Time Series (Daily)'], orient='index', dtype=np.float)
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'Data', '4. close': 'Preço', '6. volume': 'Volume'})


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)
def main():
    overview = '[OverView](https://github.com/JoseEstevan/OverView)'
    
    st.title(overview)
    st.subheader('B2W')
    
    menu = ['OverView','Ações','Sobre']
    choice = st.sidebar.selectbox("Menu",menu)
    financ = Image.open('B2W.jpg')
    
    if choice == 'OverView':
        st.markdown("A B2W (B2W Companhia Digital) é uma varejista brasileira, constituída como sociedade anônima de capital aberto e negociada na B3 sob o código BTOW3. Sua atividade principal é o comércio eletrônico. A B2W é fruto da fusão entre o Submarino e a Americanas.com. Além dessas duas marcas, estão dentro da sua operação as lojas Shoptime e Sou Barato. A companhia administra ainda serviços de pagamentos e crédito ao consumidor a partir das marcas AME, Submarino Finance e Digital Finance. A logística da companhia é centrada em mais de dez Centros de Distribuição. Esses Centros estão espalhados pelos Estados de São Paulo, Rio de Janeiro, Minas Gerais, Santa Catarina e Pernambuco.")
        st.subheader('Principais produtos e serviços comercializados pela B2W')
        st.markdown('A atividade principal da B2W é o comércio eletrônico a partir das marcas Submarino, Americanas.com, Shoptime e Sou Barato. A logística da operação da companhia funciona a partir de mais de dez Centros de Distribuição espalhados pelo Brasil. Além do comércio eletrônico, a B2W também opera sistemas de pagamentos e crédito para facilitar o acesso dos clientes aos produtos comercializados. Esses serviços são oferecidos a partir das marcas Submarino Finance, AME e Digital Finance.')
        st.image(financ, width=1200)
        d = {'Receita Líquida': [6.767,	6.488, 6.285, 8.601, 9.013, 7.963, 6.088, 4.812],'Custos': [-4.756,	-4.813,	-4.956,	-6.889,	-7.226,	-6.035,	-4.581,	-3.666], 'Lucro Líquido': [-318, -397, -411, -485, -418, -163, -159, -170], 'Ano': [20191231, 20181231, 20171231, 20161231, 20151231 ,20141231, 20131231, 20121231]}
        datad= pd.DataFrame(data=d)
        datad['Ano'] = datad['Ano'].apply(lambda x: pd.to_datetime(int(x), format="%Y%m%d"))  
        graph1 = px.line(datad,x="Ano", y="Receita Líquida", title='Receita Líquida em Bilhões', height=600, width=1000)
        st.plotly_chart(graph1) 
        
        graph2 = px.line(datad,x="Ano", y="Custos", title='Custos em Bilhões', height=600, width=1000)
        st.plotly_chart(graph2) 
        
        graph2 = px.line(datad,x="Ano", y="Lucro Líquido", title='Lucro Líquido em Milhões', height=600, width=1000)
        st.plotly_chart(graph2) 
        #st.text('Obs: Os valores com decimais estão em Bilhões, os outros estão em Milhões.')
        #st.image()
        #st.image([image1,image2])

        
    
    
    elif choice == 'Ações':
        
        df = pd.DataFrame.from_dict(doc['Time Series (Daily)'], orient='index', dtype=np.float)
        df.reset_index(inplace=True)
        df = df.rename(columns={'index': 'Data', '4. close': 'Preço', '6. volume': 'Volume'})
        
        figg = px.line(df, x='Data', y=df['Preço'], title='Valor das Ações', width=1250, height=800)
        figg.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
        ])))
        st.plotly_chart(figg)


        fig = px.line(df, x='Data', y=df['Volume'], title='Volume Negociado', width=1250, height=800)
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
        ])))
        st.plotly_chart(fig)


    elif choice == 'Sobre':
        st.header("Sobre")
        st.markdown('Esta aplicação faz parte do meu projeto OverView, que consiste em fazer análises sobre diferentes assuntos, a fim de praticar e testar coisas novas.')
        st.subheader('Redes Sociais')
        
        linkedin = '[LinkedIn](https://www.linkedin.com/in/joseestevan/)'
        st.markdown(linkedin, unsafe_allow_html=True) 
        
        github = '[GitHub](https://github.com/JoseEstevan)'
        st.markdown(github, unsafe_allow_html=True)  

        medium = '[Medium](https://joseestevan.medium.com/)'
        st.markdown(medium, unsafe_allow_html=True) 
            
    st.subheader('By: José Estevan')

if __name__ == '__main__':
    main()




