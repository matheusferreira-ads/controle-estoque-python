faturamento = 6000 # int
custo = 785
novas_vendas = 1878
faturamento = faturamento + novas_vendas
imposto = 0.15 * faturamento # float
print (imposto)


print("faturamento", faturamento)
print("custos", custo)
print("Lucro", faturamento - custo - imposto)


mensagem = "o faturamento da loja foi de 7878" # string
teve_lucro = True # booleana 



# int = numeros inteiros
# float = numeros casas decimais
# strings = textos
# boolean = booleanos (True or False) (so pode ter 2 valores)
# round = arredonda a conta ou o numero para cima

# operadores especiais 

# Mod -> % -> resto da divisão de um número pelo outro.
# Mod -> 10 % 3
print(10 % 3)

# exemplo de financiamento
anos = int(310 / 12)
anos = round(310 / 12)
print(anos, "anos")

meses = 310 % 12
print(meses, "meses")



# floor division -> // -> parte inteira da divisão 
print(310 // 12)
