{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import datetime\
\
st.set_page_config(page_title="Controle Financeiro Pessoal", layout="wide")\
\
# Inicializa\'e7\'e3o de sess\'e3o\
if 'transacoes' not in st.session_state:\
    st.session_state.transacoes = []\
\
# T\'edtulo\
st.title("Controle Financeiro Pessoal - Francisco e Renata")\
\
# Tabs principais\
aba1, aba2, aba3 = st.tabs(["Lan\'e7amentos", "Resumo Mensal", "Exportar Dados"])\
\
# Aba de Lan\'e7amentos\
with aba1:\
    st.header("Novo Lan\'e7amento")\
    col1, col2, col3 = st.columns(3)\
    with col1:\
        pessoa = st.selectbox("Pessoa", ["Francisco", "Renata"])\
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])\
        categoria = st.text_input("Categoria")\
    with col2:\
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")\
        conta = st.selectbox("Conta", ["Conta Corrente", "Cart\'e3o de Cr\'e9dito", "Investimento"])\
        data = st.date_input("Data", value=datetime.today())\
    with col3:\
        descricao = st.text_input("Descri\'e7\'e3o")\
        if st.button("Salvar Lan\'e7amento"):\
            nova_transacao = \{\
                "Pessoa": pessoa,\
                "Tipo": tipo,\
                "Categoria": categoria,\
                "Valor (R$)": valor,\
                "Conta": conta,\
                "Data": data,\
                "Descri\'e7\'e3o": descricao\
            \}\
            st.session_state.transacoes.append(nova_transacao)\
            st.success("Lan\'e7amento salvo com sucesso!")\
\
    # Visualiza\'e7\'e3o dos lan\'e7amentos\
    if st.session_state.transacoes:\
        st.subheader("Lan\'e7amentos Realizados")\
        df = pd.DataFrame(st.session_state.transacoes)\
        st.dataframe(df, use_container_width=True)\
\
# Aba de Resumo Mensal\
with aba2:\
    st.header("Resumo Mensal")\
    if st.session_state.transacoes:\
        df = pd.DataFrame(st.session_state.transacoes)\
        df['Data'] = pd.to_datetime(df['Data'])\
        df['M\'eas'] = df['Data'].dt.to_period('M')\
\
        resumo = df.groupby(['Pessoa', 'Tipo', 'M\'eas'])['Valor (R$)'].sum().reset_index()\
        st.dataframe(resumo, use_container_width=True)\
\
        st.subheader("Gr\'e1fico por Tipo")\
        grafico = resumo.pivot_table(index='M\'eas', columns=['Pessoa', 'Tipo'], values='Valor (R$)', aggfunc='sum')\
        st.line_chart(grafico)\
    else:\
        st.info("Nenhum dado lan\'e7ado ainda.")\
\
# Aba de Exporta\'e7\'e3o\
with aba3:\
    st.header("Exportar Dados")\
    if st.session_state.transacoes:\
        df = pd.DataFrame(st.session_state.transacoes)\
        csv = df.to_csv(index=False).encode('utf-8')\
        st.download_button(\
            label="Baixar como CSV",\
            data=csv,\
            file_name="controle_financeiro.csv",\
            mime="text/csv"\
        )\
    else:\
        st.info("Sem dados para exportar.")}