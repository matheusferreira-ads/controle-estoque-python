import json
import os

# Nome do arquivo onde os dados serão salvos de forma permanente
ARQUIVO_JSON = "estoque.json"

# Lista global que funcionará como o nosso "banco de dados" em memória
estoque = []

def carregar_estoque():
    """Busca os dados salvos no arquivo JSON para não perder o histórico."""
    global estoque
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
                estoque = json.load(arquivo)
            print("💾 Dados de estoque carregados com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo de salvamento: {e}")
            estoque = []
    else:
        # Se o arquivo não existe, começamos com uma lista vazia
        estoque = []

def salvar_estoque():
    """Grava as alterações da lista diretamente no arquivo JSON."""
    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            # indent=4 serve para deixar o arquivo JSON legível para humanos
            json.dump(estoque, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao salvar os dados no arquivo: {e}")

def exibir_menu():
    print("\n" + "="*30)
    print("      GERENCIADOR DE ESTOQUE")
    print("="*30)
    print("1. Cadastrar Produto")
    print("2. Listar Produtos")
    print("3. Atualizar Quantidade")
    print("4. Excluir Produto")
    print("5. Sair")
    print("="*30)

def cadastrar_produto():
    print("\n--- Cadastrar Produto ---")
    nome = input("Nome do produto: ").strip()
    
    try:
        quantidade = int(input("Quantidade em estoque: "))
        preco = float(input("Preço unitário (ex: 10.50): "))
    except ValueError:
        print("❌ Erro: Quantidade deve ser número inteiro e Preço deve ser decimal!")
        return

    produto = {
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    }
    
    estoque.append(produto)
    salvar_estoque()  # 🔄 Salva após cadastrar
    print(f"✅ Produto '{nome}' cadastrado e salvo com sucesso!")

def listar_produtos():
    print("\n--- Produtos em Estoque ---")
    if not estoque:
        print("O estoque está vazio.")
        return
    
    for i, prod in enumerate(estoque, start=1):
        print(f"{i}. {prod['nome']} | Qtd: {prod['quantidade']} | Preço: R$ {prod['preco']:.2f}")

def atualizar_quantidade():
    print("\n--- Atualizar Quantidade ---")
    listar_produtos()
    if not estoque:
        return
        
    try:
        indice = int(input("\nDigite o número do produto que deseja atualizar: ")) - 1
        if 0 <= indice < len(estoque):
            nova_qtd = int(input(f"Nova quantidade para '{estoque[indice]['nome']}': "))
            estoque[indice]['quantidade'] = nova_qtd
            salvar_estoque()  # 🔄 Salva após atualizar
            print("✅ Quantidade atualizada e salva com sucesso!")
        else:
            print("❌ Opção inválida!")
    except ValueError:
        print("❌ Erro: Digite apenas números inteiros!")

def excluir_produto():
    print("\n--- Excluir Produto ---")
    listar_produtos()
    if not estoque:
        return
        
    try:
        indice = int(input("\nDigite o número do produto que deseja excluir: ")) - 1
        if 0 <= indice < len(estoque):
            removido = estoque.pop(indice)
            salvar_estoque()  # 🔄 Salva após excluir
            print(f"✅ Produto '{removido['nome']}' removido do arquivo!")
        else:
            print("❌ Opção inválida!")
    except ValueError:
        print("❌ Erro: Digite apenas números inteiros!")

# --- INÍCIO DA EXECUÇÃO DO PROGRAMA ---
# Antes de abrir o menu, tentamos recuperar os dados salvos anteriormente
carregar_estoque()

while True:
    exibir_menu()
    opcao = input("Escolha uma opção (1-5): ").strip()
    
    if opcao == "1":
        cadastrar_produto()
    elif opcao == "2":
        listar_produtos()
    elif opcao == "3":
        atualizar_quantidade()
    elif opcao == "4":
        excluir_produto()
    elif opcao == "5":
        print("\nSaindo do sistema... Até logo!")
        break
    else:
        print("❌ Opção inválida! Tente novamente.")