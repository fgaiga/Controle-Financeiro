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

# Título
st.title("Controle Financeiro Pessoal - Francisco e Renata")

# Tabs principais
aba1, aba2, aba3, aba4 = st.tabs(["Lançamentos", "Resumo Mensal", "Exportar Dados", "Cartões de Crédito"])

# Aba de Lançamentos
with aba1:
    st.header("Novo Lançamento")
    col1, col2, col3 = st.columns(3)
    with col1:
        pessoa = st.selectbox("Pessoa", ["Francisco", "Renata"], key="pessoa_manual")
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"], key="tipo_manual")
        categoria = st.text_input("Categoria", key="categoria_manual")
    with col2:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f", key="valor_manual")
        conta = st.selectbox("Conta", ["Conta Corrente", "Cartão de Crédito", "Investimento"], key="conta_manual")
        data = st.date_input("Data", value=datetime.today(), key="data_manual")
    with col3:
        descricao = st.text_input("Descrição", key="descricao_manual")
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

    st.divider()
    st.subheader("Importar lançamentos por extrato (CSV)")
    arquivo = st.file_uploader("Escolha um arquivo .csv com colunas: Data, Descrição, Valor", type=["csv"])
    if arquivo is not None:
        try:
            df_importado = pd.read_csv(arquivo)
            df_importado.columns = [c.strip().capitalize() for c in df_importado.columns]
            if all(col in df_importado.columns for col in ["Data", "Descrição", "Valor"]):
                st.dataframe(df_importado.head())
                col1, col2 = st.columns(2)
                with col1:
                    pessoa_csv = st.selectbox("Pessoa para todos os lançamentos", ["Francisco", "Renata"], key="pessoa_csv")
                    conta_csv = st.selectbox("Conta para todos os lançamentos", ["Conta Corrente", "Cartão de Crédito", "Investimento"], key="conta_csv")
                with col2:
                    tipo_csv = st.selectbox("Tipo padrão", ["Detectar pelo valor (+/-)", "Receita", "Despesa"], key="tipo_csv")
                if st.button("Importar lançamentos"):
                    for _, row in df_importado.iterrows():
                        valor = float(row["Valor"])
                        tipo = "Receita" if valor > 0 else "Despesa"
                        if tipo_csv != "Detectar pelo valor (+/-)":
                            tipo = tipo_csv
                        transacao = {
                            "Pessoa": pessoa_csv,
                            "Tipo": tipo,
                            "Categoria": "Importado",
                            "Valor (R$)": abs(valor),
                            "Conta": conta_csv,
                            "Data": pd.to_datetime(row["Data"]).date(),
                            "Descrição": row["Descrição"]
                        }
                        st.session_state.transacoes.append(transacao)
                    st.success(f"{len(df_importado)} lançamentos importados com sucesso!")
            else:
                st.error("O arquivo deve conter as colunas: Data, Descrição, Valor")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

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

# Aba de Cartões de Crédito
with aba4:
    st.header("Cartões de Crédito")

    with st.expander("Cadastrar novo gasto no cartão"):
        col1, col2 = st.columns(2)
        with col1:
            cartao = st.selectbox("Cartão", [c['Nome'] for c in st.session_state.cartoes])
            data_compra = st.date_input("Data da compra", value=datetime.today())
            descricao = st.text_input("Descrição da compra")
        with col2:
            valor = st.number_input("Valor da compra (R$)", min_value=0.0, step=0.01, format="%.2f")
            if st.button("Salvar compra"):
                st.session_state.gastos_cartao.append({
                    "Cartão": cartao,
                    "Data": data_compra,
                    "Descrição": descricao,
                    "Valor (R$)": valor
                })
                st.success("Compra registrada com sucesso!")

    if st.session_state.gastos_cartao:
        st.subheader("Fatura do mês atual")
        df_cartao = pd.DataFrame(st.session_state.gastos_cartao)
        df_cartao['Mês'] = pd.to_datetime(df_cartao['Data']).dt.to_period('M')
        mes_atual = datetime.today().strftime('%Y-%m')
        fatura_atual = df_cartao[df_cartao['Mês'] == mes_atual[:7]]
        st.dataframe(fatura_atual, use_container_width=True)
        total_fatura = fatura_atual.groupby('Cartão')['Valor (R$)'].sum().reset_index()
        st.subheader("Total por cartão")
        st.dataframe(total_fatura, use_container_width=True)
    else:
        st.info("Nenhuma compra registrada nos cartões ainda.")
