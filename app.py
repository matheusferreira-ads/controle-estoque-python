import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# Nome do arquivo JSON
ARQUIVO_JSON = "estoque.json"

def carregar_estoque():
    """Lê os dados do arquivo JSON."""
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except:
            return []
    return []

def salvar_estoque(dados):
    """Grava os dados atualizados no arquivo JSON."""
    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"❌ Erro ao salvar no arquivo: {e}")

# --- CONFIGURAÇÃO DA PÁGINA WEB ---
st.set_page_config(page_title="Dashboard de Estoque Pro", page_icon="📦", layout="wide")

# --- INJEÇÃO DE DESIGN E CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Estilização Geral do Fundo e Fontes */
    .main {
        background-color: #f8fafc;
    }
    
    /* Título Principal */
    h1 {
        color: #1a365d !important;
        font-family: 'Arial', sans-serif;
        font-weight: 800 !important;
        padding-bottom: 10px;
    }
    
    /* Customização dos Botões Principais */
    .stButton>button {
        background-color: #1a365d !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        height: 45px;
    }
    .stButton>button:hover {
        background-color: #2b6cb0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Customização do Botão de Exclusão (Perigo) */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) .stButton>button {
        background-color: #e53e3e !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) .stButton>button:hover {
        background-color: #c53030 !important;
    }

    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 10px 20px;
        color: #4a5568;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1a365d;
        background-color: rgba(255, 255, 255, 0.5);
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #1a365d !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Estilização dos Cards de Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #1a365d !important;
    }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Layout do Cabeçalho
col_logo, col_titulo = st.columns([1, 5])
with col_titulo:
    st.title("📦 Sistema de Auditoria Preventiva e Estoque")
    st.markdown("<p style='color: #4a5568; font-size: 14px; margin-top: -15px;'>Módulo de Inteligência de Inventário conectado com foco em Prevenção de Perdas.</p>", unsafe_allow_html=True)

# Inicializa o estoque na memória do Streamlit
if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_estoque()

# --- CRIAÇÃO DAS ABAS DE NAVEGAÇÃO ---
tab_listar, tab_cadastrar, tab_gerenciar = st.tabs([
    "🔍 Painel de Controle e Alertas", 
    "➕ Cadastrar Novo Item", 
    "⚙️ Ajustar Saldos / Excluir"
])

# --- ABA 1: VISUALIZAR ESTOQUE E ALERTAS ---
with tab_listar:
    if not st.session_state.estoque:
        st.info("O estoque está vazio no momento. Vá até a aba 'Cadastrar Novo Item' para começar.")
    else:
        # --- SISTEMA DE ALERTAS INTELIGENTES ---
        hoje = date.today()
        vencidos = []
        alerta_validade = []
        
        for item in st.session_state.estoque:
            if "validade" in item:
                data_item = datetime.strptime(item["validade"], "%d/%m/%Y").date()
                if data_item < hoje:
                    vencidos.append(f"🚨 **{item['nome']}** - Vencido desde {item['validade']}")
                elif hoje <= data_item <= (hoje + timedelta(days=7)):
                    dias_restantes = (data_item - hoje).days
                    alerta_validade.append(f"⚠️ **{item['nome']}** - Vence em {item['validade']} (Restam {dias_restantes} dias)")
        
        # Exibe os blocos de alerta na tela caso existam problemas
        if vencidos or alerta_validade:
            st.subheader("📋 Alertas Críticos de Auditoria")
            col_venc, col_alerta = st.columns(2)
            
            with col_venc:
                if vencidos:
                    with st.expander("🚨 ITENS VENCIDOS NO CHÃO DE LOJA", expanded=True):
                        for v in vencidos:
                            st.error(v)
            with col_alerta:
                if alerta_validade:
                    with st.expander("⚠️ ATENÇÃO: Próximos ao Vencimento (7 dias)", expanded=True):
                        for a in alerta_validade:
                            st.warning(a)
            st.markdown("---")

        # Layout em colunas: Tabela à esquerda, Métricas à direita
        st.subheader("Visualização Geral do Inventário")
        col_tabela, col_metricas = st.columns([3, 1])
        
        with col_tabela:
            st.dataframe(
                st.session_state.estoque, 
                use_container_width=True,
                height=350,
                column_config={
                    "nome": "Nome do Produto",
                    "quantidade": st.column_config.NumberColumn("Qtd em Estoque", format="%d"),
                    "preco": st.column_config.NumberColumn("Preço Unitário", format="R$ %.2f"),
                    "validade": "Data de Validade"
                }
            )
            
        with col_metricas:
            total_itens = sum(item['quantidade'] for item in st.session_state.estoque)
            valor_total = sum(item['quantidade'] * item['preco'] for item in st.session_state.estoque)
            
            st.metric("Total de Peças/Itens", total_itens)
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Valor Total Investido", f"R$ {valor_total:,.2f}")

# --- ABA 2: CADASTRAR PRODUTO ---
with tab_cadastrar:
    st.subheader("Registrar Mercadoria no Sistema")
    
    # Criado um container branco para o formulário ficar destacado
    with st.container():
        with st.form("form_cadastro", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nome_prod = st.text_input("Nome do Produto (Descrição)").strip()
                qtd_prod = st.number_input("Quantidade Inicial", min_value=0, step=1, value=0)
            with col_f2:
                preco_prod = st.number_input("Preço de Venda Unitário (R$)", min_value=0.0, step=0.01, format="%.2f")
                validade_prod = st.date_input("Data de Validade do Lote", value=date.today(), format="DD/MM/YYYY")
            
            st.markdown("<br>", unsafe_allow_html=True)
            botao_cadastrar = st.form_submit_button("💾 Salvar e Registrar no Banco JSON")
            
            if botao_cadastrar:
                if nome_prod == "":
                    st.warning("⚠️ O nome do produto não pode ficar em branco!")
                else:
                    novo_produto = {
                        "nome": nome_prod,
                        "quantidade": int(qtd_prod),
                        "preco": float(preco_prod),
                        "validade": validade_prod.strftime("%d/%m/%Y")
                    }
                    st.session_state.estoque.append(novo_produto)
                    salvar_estoque(st.session_state.estoque)
                    st.success(f"✅ Produto '{nome_prod}' registrado com sucesso!")
                    st.rerun()

# --- ABA 3: ATUALIZAR / EXCLUIR ---
with tab_gerenciar:
    st.subheader("Ajustes Físicos e Movimentação de Estoque")
    
    if not st.session_state.estoque:
        st.info("Nenhum produto disponível para alteração.")
    else:
        nomes_produtos = [item['nome'] for item in st.session_state.estoque]
        produto_selecionado = st.selectbox("Selecione o item para modificação rápida:", nomes_produtos)
        
        idx = nomes_produtos.index(produto_selecionado)
        prod_atual = st.session_state.estoque[idx]
        
        validade_exibicao = prod_atual.get('validade', 'Não informada')
        
        # Painel informativo com o status atual do item selecionado
        st.info(f"📋 **Status Atual do Item:** Quantidade Atual: {prod_atual['quantidade']} unidades | Preço Cadastrado: R$ {prod_atual['preco']:.2f} | Validade do Lote: {validade_exibicao}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_atualizar, col_excluir = st.columns(2)
        
        with col_atualizar:
            st.markdown("### 🔄 Atualizar Saldo")
            nova_qtd = st.number_input("Informe a Nova Quantidade Real de Prateleira:", min_value=0, step=1, value=int(prod_atual['quantidade']), key="edit_qtd")
            if st.button("Confirmar Ajuste de Saldo", use_container_width=True):
                st.session_state.estoque[idx]['quantidade'] = int(nova_qtd)
                salvar_estoque(st.session_state.estoque)
                st.success("🔄 Saldo atualizado com sucesso!")
                st.rerun()
                
        with col_excluir:
            st.markdown("### 🚨 Baixa / Descarte Definitivo")
            st.write("Utilize este botão apenas em caso de quebra identificada, furto ou descarte por vencimento do produto.")
            if st.button("Remover Produto do Catálogo", use_container_width=True):
                removido = st.session_state.estoque.pop(idx)
                salvar_estoque(st.session_state.estoque)
                st.error(f"🗑️ Produto '{removido['nome']}' excluído do sistema!")
                st.rerun()