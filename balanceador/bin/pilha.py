pilhas = {}

def pilha(args):
	if len(servers) == 0:
		return False
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
	server = getMin() # ip + porta do servidor menos ocupado

	if 'nome' in args:
		if pilhas[args['nome']] in pilhas:
			return False
		else:

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

def getMin():
	sv = servers.keys()
	minimo = servers[sv[0]]
	for server in sv[1:]:
		if servers[server] < servers[minimo]:
			minimo = server
	return minimo