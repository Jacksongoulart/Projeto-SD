servers = {}

def cadastro(args):
	serverinfo = args['ip'] + ':' + args['port']
	if serverinfo in servers:
		return False
	servers[serverinfo] = 0
	print servers
	return True

def getMin():
	sv = servers.keys()
	minimo = sv[0]
	for server in sv[1:]:
		if servers[server] < servers[minimo]:
			minimo = server
	return minimo