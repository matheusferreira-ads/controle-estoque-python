import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime, date

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Sistema de Estoque Pro",
    page_icon="📦",
    layout="wide"
)

# 2. FUNÇÕES DE BANCO DE DADOS
def criar_conexao():
    return sqlite3.connect('estoque.db')

def criar_tabela():
    conn = criar_conexao()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS produtos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT, 
                  sku TEXT, 
                  quantidade INTEGER, 
                  validade DATE)''')
    conn.commit()
    conn.close()

def adicionar_produto(nome, sku, qtd, validade):
    conn = criar_conexao()
    c = conn.cursor()
    c.execute("INSERT INTO produtos (nome, sku, quantidade, validade) VALUES (?,?,?,?)",
              (nome, sku, qtd, validade))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = criar_conexao()
    df = pd.read_sql_query("SELECT * FROM produtos", conn)
    # Converter a coluna de validade para datetime para manipulação
    df['validade'] = pd.to_datetime(df['validade'])
    conn.close()
    return df

def deletar_produto(id_produto):
    conn = criar_conexao()
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
    conn.commit()
    conn.close()

# 3. LÓGICA DE NEGÓCIO
def calcular_status(data_validade):
    hoje = date.today()
    if isinstance(data_validade, str):
        validade = datetime.strptime(data_validade, '%Y-%m-%d').date()
    elif isinstance(data_validade, pd.Timestamp):
        validade = data_validade.date()
    else:
        validade = data_validade
        
    dias_restantes = (validade - hoje).days
    
    # Se vence hoje ou já venceu
    if dias_restantes <= 0:
        return "🔴 VENCIDO"
    elif dias_restantes <= 30:
        return "🟡 CRÍTICO (Próx. Vencimento)"
    else:
        return "🟢 REGULAR"

# --- INICIALIZAÇÃO ---
criar_tabela()
df = carregar_dados()
if not df.empty:
    df['Status'] = df['validade'].apply(calcular_status)

# --- BARRA LATERAL (SIDEBAR) ---
caminho_logo = "logo.jpg"
if os.path.exists(caminho_logo):
    st.sidebar.image(caminho_logo, use_container_width=True)
else:
    st.sidebar.info("Logo não encontrada")

st.sidebar.title("Navegação")
menu = ["Dashboard / Contagem", "Cadastrar Novo Item", "Relatório de Validade"]
escolha = st.sidebar.selectbox("Ir para:", menu)

# --- CORPO PRINCIPAL ---
st.title("📦 Sistema de Automação de Estoque")

# Métricas no Topo
if not df.empty:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total de Itens", len(df))
    with m2:
        vencidos = len(df[df['Status'] == "🔴 VENCIDO"])
        st.metric("Itens Vencidos", vencidos, delta=vencidos, delta_color="inverse")
    with m3:
        criticos = len(df[df['Status'].str.contains("🟡")])
        st.metric("Próximos ao Vencimento", criticos)
st.markdown("---")

# --- NAVEGAÇÃO ---
if escolha == "Dashboard / Contagem":
    st.header("📋 Controle de Inventário")
    if not df.empty:
        st.write("Gerencie as quantidades atuais abaixo:")
        
        # Formatando a data para exibição (PT-BR)
        df_exibicao = df.copy()
        df_exibicao['validade'] = df_exibicao['validade'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(
            df_exibicao[['id', 'nome', 'sku', 'quantidade', 'validade', 'Status']].sort_values(by='id'), 
            use_container_width=True
        )
        
        with st.expander("🗑️ Remover item do sistema"):
            id_para_deletar = st.number_input("Digite o ID do produto para exclusão", min_value=1, step=1)
            if st.button("Confirmar Exclusão Definitiva"):
                deletar_produto(id_para_deletar)
                st.success(f"Item ID {id_para_deletar} removido com sucesso!")
                st.rerun()
    else:
        st.info("O estoque está vazio. Use a aba de cadastro.")

elif escolha == "Cadastrar Novo Item":
    st.header("🆕 Cadastro de Produtos")
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Produto (Ex: Leite UHT)")
            sku = st.text_input("Código SKU / Barras")
        with col2:
            qtd = st.number_input("Quantidade em Estoque", min_value=0, step=1)
            # Ajuste no input para formato brasileiro
            validade = st.date_input("Data de Vencimento", min_value=date.today(), format="DD/MM/YYYY")
        
        submit = st.form_submit_button("Finalizar Cadastro")
        if submit:
            if nome and sku:
                adicionar_produto(nome.upper(), sku, qtd, validade)
                st.success(f"✅ {nome.upper()} adicionado ao sistema!")
                st.rerun()
            else:
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")

elif escolha == "Relatório de Validade":
    st.header("📅 Relatório FEFO (First Expired, First Out)")
    if not df.empty:
        filtro = st.segmented_control("Visualizar por Status:", ["Todos", "🔴 VENCIDO", "🟡 CRÍTICO (Próx. Vencimento)"], default="Todos")
        
        df_filtrado = df if filtro == "Todos" else df[df['Status'] == filtro]
        df_filtrado = df_filtrado.sort_values(by='validade')
        
        # Formatando para exibição na tabela
        df_tabela = df_filtrado.copy()
        df_tabela['validade'] = df_tabela['validade'].dt.strftime('%d/%m/%Y')
        
        st.table(df_tabela[['nome', 'validade', 'Status', 'quantidade']])
        
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Relatório em CSV",
            data=csv,
            file_name=f"relatorio_estoque_{date.today()}.csv",
            mime="text/csv",
        )
    else:
        st.info("Nenhum dado disponível.")