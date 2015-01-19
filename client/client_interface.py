from client_api import executa_operacao_api
import sys 


global funcoes 
email = "vazio@vazio.com"
funcoes = ["logar","ler_dados","editar_dado","excluir","criar"]

def main():
	print_titulo()
	global email

	while True:
		op = opcoes_iniciais()
		if	executa_operacao_inicial(op) == True:
			break

	print "Bem vindo "+email+"!\n"
	while True:
		op = opcoes_logado()
		if op == 4:
			print "\nObrigado pela preferencia :D\n"
			return
		executa_operacao(op)



def print_titulo(a=2):
	if a == 1:
		print "+-+-+-+-+-+-+-+-+"
		print "|T|e|x|t|b|o|o|k|"
		print "+-+-+-+-+-+-+-+-+"
	elif a == 2:
		print " ____ ____ ____ ____ ____ ____ ____ ____"
		print "||T |||e |||x |||t |||b |||o |||o |||k ||"
		print "||__|||__|||__|||__|||__|||__|||__|||__||"
		print "|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|"
	else: 
		print "Textbook"
	print "\n"

def executa_operacao_inicial(op):
	if op == 1:
		result = executa_operacao(0)
		if result.find("Erro") != -1:
			print result
			return False
	elif op == 2:
		result = executa_operacao(-1) 
		if result.find("Erro") != -1:
			print result
			return False
	else:
		print "Voce foi um usuario desatento ou espertinho e nao merece continuar logado!)\n"
		print "...\nVolte sempre :D \n...\nFim\n"
		exit()
	return True

def opcoes_iniciais():
	return int(raw_input("Digite:\n1 - Para logar\n2 - Criar uma conta\n"))


def opcoes_logado():
	print "Insira o numero correspondente para: \n"
	print "1 - Ler seus dados\n"
	print "2 - Editar seus dados\n"
	print "3 - Excluir sua conta\n"
	print "4 - Encerrar\n"
	sys.stdout.flush()
	return int(raw_input(""))

def executa_operacao(op):
	if op > -2 and op <4:
		(validacao,resposta) = executa_operacao_api(funcoes[op],le_dado(funcoes[op]))
		if validacao == False:
			return 'Erro: '+resposta
		else:
			resposta.read()
	else:
		return "Funcao invalida. Tente novamente.\n"

def le_dado(func):
	global email
	print "Funcao a executar: "+func
	sys.stdout.flush()
	if func == "criar":
		dados = raw_input("Insira seus dados(nome, email, senha, data de nascimento, sexo) da seguinte forma: \nnome=\"Cremilda Maria\",email=\"milda@mail.com\"...\n")
		return dados
	if func == "logar":
		email = raw_input("Insira seu endereco de email\n")
		senha = raw_input("Insira a senha\n")
		return (email,senha)
	if func == "ler_dados":
		print "Qual(is) dado(s) pretende ler?\n"
		s = raw_input("nome,email,data de nascimento (DSN),sexo,ntodos\n")
		return (email,s)
	if func == "editar_dado":
		dados = raw_input("Insira seus dados(nome, senha, data de nascimento, sexo) da seguinte forma: \nnome=\"Cremilda Maria\",email=\"milda@mail.com\"...\n")
		return (email,dados)
	if func == "excluir":
		senha = raw_input("Insira a senha\n")
		r = raw_input("Deseja mesmo excluir sua conta? (S)\n")
		if r == "S":
			return (email,senha)


print "Carregando..."
main()
