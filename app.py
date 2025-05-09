import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro Pessoal", layout="wide")

# Inicialização de sessão
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = []

# Título
st.title("Controle Financeiro Pessoal - Francisco e Renata")

# Tabs principais
aba1, aba2, aba3 = st.tabs(["Lançamentos", "Resumo Mensal", "Exportar Dados"])

# Aba de Lançamentos
with aba1:
    st.header("Novo Lançamento")
    col1, col2, col3 = st.columns(3)
    with col1:
        pessoa = st.selectbox("Pessoa", ["Francisco", "Renata"])
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        categoria = st.text_input("Categoria")
    with col2:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
        conta = st.selectbox("Conta", ["Conta Corrente", "Cartão de Crédito", "Investimento"])
        data = st.date_input("Data", value=datetime.today())
    with col3:
        descricao = st.text_input("Descrição")
        if st.button("Salvar Lançamento"):
            nova_transacao = {
                "Pessoa": pessoa,
                "Tipo": tipo,
                "Categoria": categoria,
                "Valor (R$)": valor,
                "Conta": conta,
                "Data": data,
                "Descrição": descricao
            }
            st.session_state.transacoes.append(nova_transacao)
            st.success("Lançamento salvo com sucesso!")

    # Visualização dos lançamentos
    if st.session_state.transacoes:
        st.subheader("Lançamentos Realizados")
        df = pd.DataFrame(st.session_state.transacoes)
        st.dataframe(df, use_container_width=True)

# Aba de Resumo Mensal
with aba2:
    st.header("Resumo Mensal")
    if st.session_state.transacoes:
        df = pd.DataFrame(st.session_state.transacoes)
        df['Data'] = pd.to_datetime(df['Data'])
        df['Mês'] = df['Data'].dt.to_period('M')

        resumo = df.groupby(['Pessoa', 'Tipo', 'Mês'])['Valor (R$)'].sum().reset_index()
        st.dataframe(resumo, use_container_width=True)

        st.subheader("Gráfico por Tipo")
        grafico = resumo.pivot_table(index='Mês', columns=['Pessoa', 'Tipo'], values='Valor (R$)', aggfunc='sum')
        st.line_chart(grafico)
    else:
        st.info("Nenhum dado lançado ainda.")

# Aba de Exportação
with aba3:
    st.header("Exportar Dados")
    if st.session_state.transacoes:
        df = pd.DataFrame(st.session_state.transacoes)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar como CSV",
            data=csv,
            file_name="controle_financeiro.csv",
            mime="text/csv"
        )
    else:
        st.info("Sem dados para exportar.")