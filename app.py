# trecho anterior mantido

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
        if not resumo.empty:
            grafico = resumo.pivot_table(index='Mês', columns=['Pessoa', 'Tipo'], values='Valor (R$)', aggfunc='sum')
            if not grafico.empty:
                st.line_chart(grafico)
            else:
                st.info("Ainda não há dados suficientes para gerar o gráfico.")
        else:
            st.info("Ainda não há dados suficientes para gerar o gráfico.")
    else:
        st.info("Nenhum dado lançado ainda.")

# (continua com exportação e cartões...)