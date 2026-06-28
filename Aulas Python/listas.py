# Para se criar uma lista sempre terá que abrir -> []

lista_vendas = [100, 50, 1000, 800, 35]

print(lista_vendas[0]) #para pegar um item da lista

# TAMANHO DA LISTA

quantidade_vendas = len(lista_vendas)
print("quantidade_vendas")

# SOMAR TODOS OS ITENS 

total_vendas = sum(lista_vendas)
print(total_vendas)

# VALOR MÁXIMO, MÍNIMO E MÉDIA

print(max(lista_vendas))
print(min(lista_vendas))
print(total_vendas / quantidade_vendas)

# ENCONTRAR UM ELEMENTO (A POSIÇÃO DO ELEMENTO NA LISTA)

lista_produtos = ["iphone", "ipad", "apple watch", "airpod", "macbook"]
print("airpod" in lista_produtos)

posicao = lista_produtos.index("airpod")
print(posicao)

pedaco_lista = lista_produtos[posicao:]
print(pedaco_lista)