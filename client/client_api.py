from client_http import client

ip = "http://localhost:8001/"

'''
	operacao?campo="valor"
	String para passar para enviar: end_ip/addUser?email="email@email"&senha="123"&...
	funcoes:
		addUser -> manda os dados que tiver enviado (obrigatoriamente email e senha)
		deleteUser -> manda o email,senha
		loginUser -> email,senha
		readUser -> 
			[lista de dados que quer ler]		
			end_ip/readUser?email=valor@valor.com&campos="nome|email|senha|..."
		updateUser -> 
			end_ip/updateUser?email=valor@valor.com&nome="novonome"&....
	
'''


# Retorna um response dado pelo client com a url gerada por uma funcao
def executa_operacao_api(op,dados):
	funcoes = {'criar': criar, 'logar': logar, 'ler_dados': ler_dados, 'editar_dado': editar,'excluir': excluir }
	if op in funcoes:
		(validacao, result) = funcoes[op](dados)
		if validacao == True:
			return client(result)
		else:
			return (False,result)
	else:
		return (False,"Funcao nao suportada pela API")

#recebe uma string do tipo "campo1=valor1,campo2=valor2..."
def criar(dados):
	global ip
	if (dados.find("email") == -1 ) or (dados.find("senha")==-1):
		return (False, "Email e senha sao obrigatorios na criacao, tente novamente...\n")
	dados = dados.replace(',','&')
	url = ip+"addUser?"+dados
	return (True,url)

#recebe uma tupla do tipo (email,senha)
def logar(dados):
	global ip
	(email,senha) = dados
	url = ip+"loginUser?email="+email+"&senha="+senha
	return (True,url)


#recebe uma tupla do tipo (email,campos), com campos = "campo1,campo2,campo3..."
def ler_dados(dados):
	global ip
	(email,campos) = dados
	campos = campos.replace(",","|")
	url = ip+"readUser?"+"email="+email+"&campos="+campos
	return (True,url)

#recebe uma tupla do tipo (email,campos), com campos = "nome=valor1,senha=valor2,..."
def editar(dados):
	global ip
	(email,campos) = dados
	if campos.find("email")!=-1:
		return(False,"Email nao pode ser alterado\n")
	campos = campos.replace(",","&")
	url = ip+"updateUser?email="+email+"&"+campos
	return (True, url)


#recebe uma tupla do tipo (email,senha)
def excluir(dados):
	global ip
	(email,senha) = dados
	url = ip+"deleteUser?"+"email="+email+"&"+"senha="+senha
	return (True,url)

# print excluir(("aa@aa","123"))
	
	

# executa_operacao_api('criar','email=julia@julia&senha=123')