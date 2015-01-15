import signal  # Signal support (server shutdown on signal receive)
import argparse
import sys
sys.path.append('../client/')
sys.path.append('../server/')
sys.path.append('bin')
from pythonserver import *
import pythonclient
import cadastro

class LoadBalancer(PythonServer):

	def __init__(self, port):
		PythonServer.__init__(self, port)

	def wait_for_connections(self):
		print "Waiting for connections balancer"
		while True:
			self.socket.listen(5) # numero maximo de conexoes na fila
			request = RequestHandlerBalancer(self.socket.accept())
			request.start()

##################################################################################


class RequestHandlerBalancer(RequestHandler):

	def __init__(self, (conn, addr)):
		RequestHandler.__init__(self, (conn, addr))

	def make_url(self, s, server_key):
		lines = s.split('\n')
		tokens = lines[0].split(' ')
		protocol = tokens[0]
		directory = tokens[1]
		if protocol == "GET":
			return server_key+directory
		elif protocol == "POST":
			return server_key+directory+'?'+lines[len(lines)-1]
		else:
			return False

	def GET(self, string):
		server = cadastro.getMin()
		cadastro.servers[server] = cadastro.servers[server] + 1
		request = self.make_url(string, server)
		response_content = pythonclient.client(request)
		self.conn.send(response_content)

	def POST(self, string):
		request = string.split(' ') # Separa no espaco e pega o segundo elemento: '/modulo'
		module = request[1].split('/')[1] # Separa na funcao chamada: modulo
		args = request[len(request)-1].split('\n') # Separa nas quebras de linha do ultimo elemento do request
		args = args[len(args)-1].split('&')  # Pega a ultima posicao e separa pelo '&'
		arguments = {}
		for i in range(len(args)):
		    arg = args[i].split('=')
		    arguments[arg[0]] = arg[1]
		newDir = self.www_dir + '/bin/'
		file_path = newDir + module + '.py'
		sys.path.append(newDir)
		if os.path.isfile(file_path):
		    mod = __import__(module)
		    ret = getattr(mod, module)(arguments)
		    response = 'HTTP/1.0 200 OK\nContent-Type: text/html;charset=utf-8\n\n<html>'+str(ret)+'</html>\n'
		else:
		    response = 'HTTP/1.0 404 NOT FOUND'
		self.conn.send(response)




#############################################################	


def graceful_shutdown(sig, dummy):
    s.shutdown()

def get_parameters():
    parser = argparse.ArgumentParser(description='Http Load Balancer')
    parser.add_argument('port', metavar='port', type=int,
                       help='The port for the Load Balancer to listen')
    return parser.parse_args()

#############################################################

signal.signal(signal.SIGINT, graceful_shutdown)
args = get_parameters()
print "Starting Load Balancer"
s = LoadBalancer(args.port)
s.activate_server()
s.wait_for_connections()