import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro Pessoal", layout="wide")

# Inicialização de sessão
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = []
if 'cartoes' not in st.session_state:
    st.session_state.cartoes = [
        {'Nome': 'Cartão Francisco', 'Pessoa': 'Francisco', 'Limite': 10000.00},
        {'Nome': 'Cartão Renata', 'Pessoa': 'Renata', 'Limite': 8000.00}
    ]
if 'gastos_cartao' not in st.session_state:
    st.session_state.gastos_cartao = []
if 'categorias' not in st.session_state:
    st.session_state.categorias = [
        "Alimentação", "Transporte", "Moradia", "Educação", "Saúde", "Lazer",
        "Viagens", "Combustível", "Financiamentos", "Investimentos",
        "Distribuição Lucro", "Baixa Investimento", "Seguros"
    ]

# Título
st.title("Controle Financeiro Pessoal - Francisco e Renata")

# Botão para limpar todos os lançamentos
if st.button("🧹 Limpar todos os lançamentos"):
    st.session_state.transacoes.clear()
    st.success("Todos os lançamentos foram removidos da sessão.")

# Tabs principais
aba1, aba2, aba3, aba4 = st.tabs(["Lançamentos", "Resumo Mensal", "Exportar Dados", "Cartões de Crédito"])

# Aba de Lançamentos
with aba1:
    st.header("Novo Lançamento")

    with st.expander("Cadastrar nova categoria"):
        nova_categoria = st.text_input("Nome da nova categoria")
        if st.button("Adicionar categoria"):
            if nova_categoria and nova_categoria not in st.session_state.categorias:
                st.session_state.categorias.append(nova_categoria)
                st.success("Categoria adicionada com sucesso!")
            else:
                st.warning("Categoria inválida ou já existente.")

    col1, col2, col3 = st.columns(3)
    with col1:
        pessoa = st.selectbox("Pessoa", ["Francisco", "Renata"])
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        categoria = st.selectbox("Categoria", st.session_state.categorias)
    with col2:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
        conta = st.selectbox("Conta", [
            "Conta Corrente Francisco", "Conta Corrente Renata",
            "Cartão de Crédito Francisco", "Cartão de Crédito Renata",
            "Investimento Francisco", "Investimento Renata"
        ])
        data = st.date_input("Data", value=datetime.today())
    with col3:
        descricao = st.text_input("Descrição")
        if st.button("Salvar Lançamento"):
            if valor > 0:
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
            else:
                st.warning("O valor precisa ser maior que zero.")

    if st.session_state.transacoes:
        st.subheader("Lançamentos Realizados")
        df = pd.DataFrame(st.session_state.transacoes)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum lançamento registrado ainda.")