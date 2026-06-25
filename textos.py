faturamento = 1000
custo = 600

lucro = faturamento - custo

# primeira forma de fazer - texto = "o lucro foi de " + str(lucro) + " e o faturamento foi de " + str(faturamento)


# segunda forma de fazer - texto = f"o lucro foi de {lucro} e o faturamento foi de {faturamento}"
# colocar tudo dentro do texto e colocar a letra "f" de format antes do texto. Exemplo:
texto = f"o lucro foi de {lucro} e o faturamento foi de {faturamento}"

print(texto)

email = " EMAIL_FALSO@gmail.com "
# se quiser padronizar tudo em letras minusculas só inserir o comando .lower(). Exemplo:

print(email.lower())

# caso queira corrigir erros de espaçamentos, só inserir o comando .strip(). Exemplo:
# email = " email_falso@gmail.com "

print(email.strip())

# caso queira editar o texto por completo retirando espaçamentos e padronizando, terá que digitar a variável.

email = email.lower() # colocar em letra minuscula
email = email.strip() # ajustar espaços vazios
print(email) 

# TAMANHO
# para saber quantos caracteres tem, só inserir o comando len. Exemplo:

print(len(email))

# POSIÇÃO
# para saber onde está um determinado caracter dentro do texto usamos o comando .find(). Exemplo:

posicao = email.find("@")
print(posicao)
# se tiver mais de um caracter no mesmo texto, o comando vai sempre mostar
# a posição da primeira insidência que aparece no texto. Exemplo:

posicao = email.find("@")
print(posicao)

# PEDAÇOS DO TEXTO
# para pegar pedaços do texto a partir de onde você quer, basta inserir o numero da posição do caracter que você quer 
# e colocar entre []. Exemplo:

print(email[11])

# caso queira pegar um pedaço maior do texto, basta inserir : Exemplo:

print(email[11:21])

# OU 
print(email[11:])

# OU caso queira fazer de forma automática, basta incluir a variável "posicao". Exemplo:
servidor = email[posicao:]
print(servidor)

# funiona também ao inverso. Ex: [:posicao]

# trocar um pedaço do texto 
# sempre que quiser editar o texto usar o .replace(). Se quiser editar o texto, lembrar de colocar o testo que quer editar .oque quer fazer
# exemplo:
novo_email = email.replace("gmail.com" , "yahoo.com.br")
print(novo_email)

# se quiser subsituir uma determinada quantidade de vezes, somente colocar "," e o número de vezes que quer subsituir. 

# COLOCANDO EM CAPSLOCK 

# Se quiser colocar o texto em capslock sempre colocar .capitalize() - Exemplo:
nome = "matheus ferreira"
nome = nome.capitalize()
print(nome)

# se quiser a primeira letra maiúscula de cada palavra, usar o comando .tile() - Exemplo:
nome = nome.title()
print(nome)

# se quiser todas a letras maiúsculas, utilizar o comando .upper() = Exemplo:
nome = nome.upper()
print(nome)

# FORMATAÇÃO NUMÉRICA
faturamento = 1,000,000 # numero inteiro mas como vai ser um numero decimal, então terá que colocar f. Como o numero tem 2 casas decimais, enão terá que colocar .2f
custo = 600


# EXERCÍCIOS
nome = "joao paulo lira"
email = "emailfalsodolira@gmail.com"

# 1 - DESCUBRA O SERVIDOR O EMAIL

posicao = email.find("@")
servidor = email[posicao:]
print(servidor)

# 2 - DESCUBRA O PRIMEIRO NOME DO USUÁRIO

posicao_espaco = nome.find(" ")
primeiro_nome = nome[:posicao_espaco]
primeiro_nome = primeiro_nome.capitalize()
print(primeiro_nome)

# 3 - CRIAR UMA MENSAGEM PERSONALIZADA DIZENDO "USUÁRIO 1º NOME FOI CADASTRADO COM SUCESSO NO EMAIL"

mensagem = f"Usuario {primeiro_nome} foi cadastrado com sucesso no email {email}"
print(mensagem)