import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Vendas.xlsx")
    
    return df

def main():
    
    st.set_page_config(page_title="Imersão", layout="wide")
    
    df = carregar_dados()
    
    st.title("Dashboard de vendas 📊")
    
    ano_filtrado = st.sidebar.selectbox("Filtra por ano:",["Todos", *df["Ano"].unique()])
    
    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
    else:
        df_filtrado = df
    
    col1,col2,col3 = st.columns(3)
    
    with col1:
        total_custo = f'{df_filtrado["Custo"].sum():,.2f}'
        st.metric("Total Custo", f"{total_custo}")
        #col1.metric("Total", f"R$ {total_custo[:2]}.{total_custo[2:5]}.{total_custo[5:]}")
    
    with col2:
        total_lucro = f'{df_filtrado["Lucro"].sum():,.2f}'
        st.metric("Total Lucro", f"{total_lucro}")
        #col2.metric("Total", f"R$ {total_lucro[:2]}.{total_lucro[2:5]}.{total_lucro[5:]}")
        
    with col3:
        total_clientes = df_filtrado["ID Cliente"].nunique()
        st.metric("Total Clientes", f"{total_clientes}")
        #col3.metric("Total", f"{total_clientes}")
        
        
    
    col1,col2 = st.columns(2)        
    
    total_vendidos_produtos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().sort_values(ascending=True).reset_index()
    
    with col1:
        fig = px.bar(total_vendidos_produtos_marca, y="Marca", x="Quantidade", orientation="h", title="Total de produtos vendidos por Marca", text="Quantidade",width=400, height=350)
        fig.update_layout(title_x=0.2)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.pie(lucro_categoria, values="Lucro", names="Categoria", title="Lucro por Categoria", hole=0.6, color_discrete_sequence=["#FF0000","#008000","#0000FF"], width=400, height=350)
        fig.update_layout(title_x=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
    
    lucro_mes_categoria = df_filtrado.groupby(["mes_ano","Categoria"])["Lucro"].sum().reset_index()
    fig_lucro_mes_categoria = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", title="Lucro x Mes x Categoria", color="Categoria", markers=True, color_discrete_sequence=["#FF0000","#008000","#0000FF"])
    fig_lucro_mes_categoria.update_layout(title_x=0.45)
    st.plotly_chart(fig_lucro_mes_categoria, use_container_width=True)
    
    style_metric_cards(border_left_color="#7B68EE")
    
    st.markdown(
    """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 18px;
            color: rgba(0,0,0,0,)
        }
        </style>
    """,
    unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()