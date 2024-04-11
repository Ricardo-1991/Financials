import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import io
import requests
from io import BytesIO

# Setup our colours
color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
'#008941', '#006FA6', '#A30059','#FFDBE5', '#7A4900',
'#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF',
'#997D87', '#5A0007', '#809693', '#FEFFE6', '#1B4400',
'#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A',
'#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9',
'#B903AA', '#D16100', '#DDEFFF', '#000035', '#7B4F4B',
'#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
'#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744',
'#C0B9B2', '#C2FF99', '#001E09', '#00489C', '#6F0062',
'#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1',
'#788D66', '#885578', '#FAD09F', '#FF8A9A', '#D157A0',
'#BEC459', '#456648', '#0086ED', '#886F4C', '#34362D',
'#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9',
'#FF913F', '#938A81', '#575329', '#00FECF', '#B05B6F',
'#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
'#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C',
'#772600', '#D790FF', '#9B9700', '#549E79', '#FFF69F',
'#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465',
'#922329', '#5B4534', '#FDE8DC', '#404E55', '#0089A3',
'#CB7E98', '#A4E804', '#324E72', '#6A3A4C'
]


club_image_paths = {'América': 'https://github.com/JAmerico1898/Financials/tree/main/America.png',
              'Athletico': 'https://raw.githubusercontent.com/JAmerico1898/Financials/tree/main/Athletico.png',
              'Atlético': 'https://raw.githubusercontent.com/JAmerico1898/Financials/blob/main/Atletico.png',
              'Bahia': 'https://github.com/JAmerico1898/Financials/blob/main/Bahia.png',
              'Botafogo': 'https://github.com/JAmerico1898/Financials/blob/main/Botafogo.png',
              'Corinthians': 'https://github.com/JAmerico1898/Financials/blob/main/Corinthians.png',
              'Coritiba': 'https://github.com/JAmerico1898/Financials/blob/main/Coritiba.png',
              'Cruzeiro': 'https://github.com/JAmerico1898/Financials/blob/main/Cruzeiro.png',
              'Cuiabá': 'https://github.com/JAmerico1898/Financials/blob/main/Cuiaba.png',
              'Flamengo': 'https://github.com/JAmerico1898/Financials/blob/main/Flamengo.png',
              'Fluminense': 'https://github.com/JAmerico1898/Financials/blob/main/Fluminense.png',
              'Fortaleza': 'https://github.com/JAmerico1898/Financials/blob/main/Fortaleza.png',
              'Goiás': 'https://github.com/JAmerico1898/Financials/blob/main/Goias.png',
              'Grêmio': 'https://github.com/JAmerico1898/Financials/blob/main/Gremio.png',
              'Internacional': 'https://github.com/JAmerico1898/Financials/blob/main/Internacional.png',
              'Palmeiras': 'https://github.com/JAmerico1898/Financials/blob/main/Palmeiras.png',
              #'Red Bull': 'https://github.com/JAmerico1898/Financials/blob/main/RedBull.png',
              'Santos': 'https://github.com/JAmerico1898/Financials/blob/main/Santos.png',
              'São Paulo': 'https://github.com/JAmerico1898/Financials/blob/main/SaoPaulo.png',
              'Vasco': 'https://github.com/JAmerico1898/Financials/blob/main/Vasco.png'}


# Loading base file
df = pd.read_excel("Balanços - clubes.xlsx", sheet_name="Resultado")
df2 = pd.read_excel("Balanços - clubes.xlsx", sheet_name="Caixa")
df1 = pd.read_excel("Balanços - clubes.xlsx", sheet_name="Índices")
clubs = pd.read_excel("clubes.xlsx")

# Defining clubes
clubes = ["América", "Athletico", "Atlético", "Bahia", "Botafogo", 
          "Corinthians", "Coritiba", "Cruzeiro", "Cuiabá", "Flamengo", 
          "Fluminense", "Fortaleza", "Grêmio", "Goiás", "Internacional", 
          "Palmeiras", "Santos", "São Paulo", "Vasco"]

# Defining labels_resultado
label = ["Direitos de transmissão", "Publicidade e patrocínio", "Arrecadação de jogos", 
         "Sócio-torcedor", "Premiações", "Licenciamento da marca", "RECEITA RECORRENTE", 
         "Negociação de atletas", "Outras receitas", "RECEITA OPERACIONAL LÍQUIDA", 
         "Pessoal e encargos sociais", "Direitos de imagem", "Despesas com jogos", 
         "Despesas gerais e administrativas", "Depreciação e amortização", "Outras despesas", 
         "DESPESAS", "RESULTADO OPERACIONAL", "Resultado financeiro", "RESULTADO"]

# Defining labels_caixa
label_caixa = ["Direitos de transmissão", "Publicidade e patrocínio", "Arrecadação de jogos", 
         "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas", 
         "GERAÇÃO DE CAIXA TOTAL", "SAÍDAS DE CAIXA OPERACIONAIS", "Pessoal e encargos sociais", 
         "Direitos de imagem", "Despesas com jogos", "Despesas gerais e administrativas", 
         "Outras despesas", "Ajuste na Geração de Caixa Operacional", "GERAÇÃO DE CAIXA OPERACIONAL", 
         "CAIXA DESTINADO A INVESTIMENTOS", "Compra de Jogadores", "Compra de Imobilizado", "Outras", 
         "CAIXA DESTINADO A FINANCIAMENTOS", "AUMENTO/DIMINUIÇÃO DE CAIXA"]

# Defining temas contábeis
temas_cont = ["Receita c/ Direitos de Transmissão", "Receita c/ Publicidade e patrocínio", 
         "Receita de Match-Day", "Receita de Sócio-torcedor", "Premiações", 
         "Receita c/ Licenciamento da marca", "Receita Recorrente", "Receita c/ Negociação de Atletas", 
         "Receita Operacional Líquida", "Despesas com Operação de Jogos", 
         "Despesas Gerais e Administrativas", "Resultado", "Geração de Caixa Operacional", 
         "EBITDA", "Dívida", "Aquisições de atletas"]

# Defining temas gerenciais
temas_ger = ["Folha do Futebol", "Base de Torcedores", "Pontuação Série A 2023", 
         "Performance Série A 2023", "Bilheteria Série A 2023 (R$ milhões)", "Bilheteria média (R$ mil/jogo)", 
         "Público Médio (pagantes)", "Sócios-Torcedores", "Público Médio / Sócios-Torcedores (%)", 
         "Valor do Elenco (€ milhões)"]


# Defining temas
temas_y = ["Receita c/ Direitos de transmissão", "Receita c/ Publicidade e patrocínio", 
           "Receita de Match-Day", "Receita de Sócio-torcedor", "Premiações", 
           "Receita c/ Licenciamento da marca", "Receita Recorrente", 
           "Receita c/ Negociação de atletas", "Receita Operacional Líquida", "Folha do futebol", 
           "Despesas com Operação de jogos", "Despesas gerais e administrativas", "Resultado", 
           "Geração de Caixa Operacional", "EBITDA", "Dívida", "Aquisições de atletas", 
           "Despesas Operacionais c/ Base"]

# Defining temas
temas_x = ["Base de Torcedores", "Pontuação Série A 2023", 
           "Performance Série A 2023", "Bilheteria Série A 2023 (R$ mil)", 
           "Bilheteria média (R$ mil/jogo)", "Público Médio (pagantes)", "Sócios-Torcedores", 
           "Público Médio / Sócios-Torcedores", "PIB do Estado (R$ bilhões)"]

with st.sidebar:
    choose = option_menu("Galeria de Apps", ["Análise Individual", "Análise Comparativa Univariada", "Análise Comparativa Bivariada"],
                         icons=['graph-up-arrow', 'magic', 'book'],
                         menu_icon="app-indicator", default_index=0, 
                         styles={
                         "container": {"padding": "5!important", "background-color": "#fafafa"},
                         "icon": {"color": "orange", "font-size": "25px"},
                         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                         "nav-link-selected": {"background-color": "#02ab21"},    
                         }
                         )

###############################################################################################################################

if choose == "Análise Individual":
    clube = st.selectbox("Escolha o Clube", options=clubes)
    fontsize = 24
    if clube == "Palmeiras":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 16, 16, 16, 16, 16, 16, 17, 17] #19 sources
        target = [6, 6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19], np.r_[16]] #19 values
        dfa = df.iloc[:, np.r_[16]]
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.85, 0.95, 0.95]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.13, 0.20, 0.40, 0.00, -0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.00, -0.20, -0.20, 0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'blue', 'steelblue', 'steelblue', 'blue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'blue', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'LightSkyBlue', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.295, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.30, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=1.24, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.15, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=1.04, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.855, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.80, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.87, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.01, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.96, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14, 15, 15, 15, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13,  8, 16, 20, 21, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 21, 17, 18, 19], np.r_[16]] #19 values
        dfa = df2.iloc[:, np.r_[16]]
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.78]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.65]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'steelblue', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=0.92, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.83, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.39, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.28, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        st.plotly_chart(fig)















#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Flamengo":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 16, 16, 16, 16, 16, 16, 17, 17] #19 sources
        target = [6, 6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19], np.r_[10]] #19 values
        dfa = df.iloc[:, np.r_[10]]
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.85, 0.95, 0.95]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.13, 0.20, 0.40, 0.00, -0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.00, -0.20, -0.20, 0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'blue', 'steelblue', 'steelblue', 'blue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'blue', 'steelblue', 'steelblue']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'LightSkyBlue', 'LightSkyBlue']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.285, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.30, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=1.24, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.15, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=1.04, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.855, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.80, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.865, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.96, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.06, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.97, y=1.02, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 8, 15, 15, 15, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 21, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 21, 17, 18, 19], np.r_[16]] #19 values
        dfa = df2.iloc[:, np.r_[10]]
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.78]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.65]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'steelblue', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=0.92, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.83, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.39, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.28, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        st.plotly_chart(fig)




























###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

elif choose == "Análise Comparativa Univariada":

    tema_cont = st.selectbox("Escolha o Tema Contábil", options=temas_cont)
    fontsize = 24
    if tema_cont == "Receita c/ Direitos de Transmissão":
        tópico = df1.iloc[0, 1:].values
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                return OffsetImage(img, zoom=1.25)
            except Exception as e:
                print(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_url = club_image_paths.get(club)
            #st.write(img_url)
            if img_url:
                img = getImage(img_url)
                st.write(img)
                if img:
                    st.write(img)
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita c/ Publicidade e patrocínio":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[1, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita de Match-Day":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[2, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita de Sócio-torcedor":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[3, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Premiações":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[4, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita c/ Licenciamento da marca":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[5, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita Recorrente":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[6, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita c/ Negociação de Atletas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[7, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Receita Operacional Líquida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[9, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Despesas com Operação de Jogos":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[12, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Despesas Gerais e Administrativas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[13, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Resultado":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[17, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Geração de Caixa Operacional":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[18, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "EBITDA":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[19, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Dívida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[20, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_cont == "Aquisições de atletas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[22, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

    tema_ger = st.selectbox("Escolha o Tema Gerencial", options=temas_ger)
    fontsize = 24
    if tema_ger == "Folha do Futebol":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[26, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Base de Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[28, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Pontuação Série A 2023":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[29, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Bilheteria Série A 2023 (R$ milhões)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[31, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Bilheteria média (R$ mil/jogo)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[32, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Público Médio (pagantes)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[33, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=14)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Sócios-Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[34, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=14)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Público Médio / Sócios-Torcedores (%)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[35, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height*100:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Valor do Elenco (€ milhões)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[37, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(path):
            try:
                return OffsetImage(plt.imread(path), zoom=1.25)
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


elif choose == "Análise Comparativa Bivariada":
    fontsize = 24
    #markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema:}</div>"
    st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Bivariada</b></h4>", unsafe_allow_html=True)
    #st.markdown(markdown_1, unsafe_allow_html=True)
    st.markdown("---")

    eixo_x = st.selectbox("Escolha o primeiro Tema (eixo horizontal)", options=temas_x)           #tópico = df1.iloc[24, 1:].values
    eixo_y = st.selectbox("Escolha o primeiro Tema (eixo vertical)", options=temas_y)
    if eixo_x:
        # Filtering the row where column 0 matches the category (eixo_x)
        filtered_row_x = df1.loc[df1.iloc[:, 0] == eixo_x]
        # Capturing columns "1:" from the filtered row
        result_x = filtered_row_x.iloc[:, 1:].values.flatten()  # Flattening the result for easy handling
        if eixo_y:
            # Filtering the row where column 0 matches the category (eixo_x)
            filtered_row_y = df1.loc[df1.iloc[:, 0] == eixo_y]
            # Capturing columns "1:" from the filtered row
            result_y = filtered_row_y.iloc[:, 1:].values.flatten()  # Flattening the result for easy handling

            # Plotting using "fig"
            fig, ax = plt.subplots(figsize=(8, 6))

            club_image_paths = {club: f'C:/Users/degef.antunes/Desktop/JoséAmérico/Python_Projects/Financials/{club}.png' for club in clubs.iloc[:, 0].unique()}
            def getImage(path):
                try:
                    return OffsetImage(plt.imread(path), zoom=0.65)
                except FileNotFoundError:
                    print(f"File not found: {path}")
                    return None

            # Modify this part of your plotting code
            for i, club in enumerate(df1.columns[1:]):
                img_path = club_image_paths.get(club)
                #st.write(img_path)
                #st.write(club)
                if img_path:
                    img = getImage(img_path)
                    #st.write(img)
                    if img:
                        # Get the index for the selected categories (eixo_x, eixo_y)
                        x = result_x[i]
                        #st.write(x)
                        y = result_y[i]
                        #st.write(y)
                        ab = AnnotationBbox(img, (x, y), frameon=False)
                        ax.add_artist(ab)
                    else:
                        print(f"Failed to load image for {club}")

            # Plotting using "fig"
            ax.scatter(result_x, result_y, color='green', alpha=0.5)
            ax.set_title(f'{eixo_x} vs {eixo_y}', fontsize=16, fontweight='bold')
            ax.set_xlabel(eixo_x, fontsize=14, fontweight='bold')
            ax.set_ylabel(eixo_y, fontsize=14, fontweight='bold')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.set_ylim([min(result_y) - 1, max(result_y) + 20])
            current_ticks = ax.get_xticks()
            ax.set_xticklabels([f'{int(tick)}' for tick in current_ticks])

            plt.tight_layout()
            st.pyplot(fig)

















