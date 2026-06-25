faturamento = input("preencha o o fauramento (apenas números)") # a informação do input sempre virá como texto e não como números
faturamento = float(faturamento)
custo = 600

lucro = faturamento - custo

print(lucro)

vendas_dia1 = float(input("vendas dia 1:"))
vendas_dia2 = float(input("vendas dia 2:"))

print(vendas_dia1 + vendas_dia2)