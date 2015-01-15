import json

pilhas = {}

def pilha(args):
	functions = {'criar': criar,
				 'zerar': zerar,
				 'push': push,
				 'pop': pop,
				 'dump': dump
				 }
	funcao = args['funcao']
	del args['funcao']
	if funcao in functions:
		return functions[funcao](args)
	else:
		return 'Undefined action'

def criar(args):
	if 'nome' in args:
		pilhas[args['nome']] = []
		return True
	return False

def zerar(args):
	if 'nome' in args and args['nome'] in pilhas:
		pilhas[args['nome']] = []
		return True
	return False

def push(args):
	if 'nome' in args and 'dado' in args and args['nome'] in pilhas:
		pilhas[args['nome']].append(args['dado'])
		return True
	return False

def pop(args):
	if 'nome' in args and args['nome'] in pilhas:
		return pilhas[args['nome']].pop()
	return False

def dump(args):
	if 'nome' in args and args['nome'] in pilhas:
		return json.dumps(pilhas[args['nome']])
	return False