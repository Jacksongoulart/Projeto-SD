import socket  # Networking support
import sys
import signal
sys.path.append('../banco/')
from userDB import *
import threading
import os
import os.path

class PythonServer:

    def __init__(self, port, serversNumber, identifier, serverMap, dir='.'):
        """ Constructor """
        self.serverMap = serverMap
        self.serversNumber = serversNumber
        self.identifier = identifier
        self.host = ''
        self.port = port
        self.www_dir = dir # Diretorio do servidor

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Launching HTTP server on port", self.port
        try:
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print "Unable to serve at port", self.port
            self.shutdown()

        print "Server successfully acquired the socket with port:", self.port
        print "Press Ctrl+C to shut down the server and exit."

    def shutdown(self):
        try:
            print "Shutting down the server"
            s.socket.shutdown(socket.SHUT_RDWR)
            s.socket.close
        except Exception as e:
            print "Could not shut down the socket:", e.stderr
        finally:
            sys.exit(1)

    def wait_for_connections(self):
        print "Waiting for connections server"
        while True:
            self.socket.listen(5) # numero maximo de conexoes na fila
            request = RequestHandler(self.socket.accept(), self.serversNumber, self.identifier, self.serverMap, self.www_dir)
            request.start()

#########################################################################

class RequestHandler(threading.Thread):
	def __init__(self, (conn, addr), serversNumber, identifier, serverMap, www_dir='.'):
	    threading.Thread.__init__(self)
	    self.serversNumber = serversNumber
	    self.identifier = identifier
	    self.serverMap = serverMap
	    self.conn = conn
	    self.addr = addr
	    self.size = 1024
	    self.www_dir = www_dir
	    print "Got connection from:", addr

	def run(self):
	    data = self.conn.recv(self.size)	#recebe os dados do cliente
	    string = bytes.decode(data) 		#decodifica em string

	    request_method = string.split(' ')[0]
	    methods = {
	  	# aqui eu coloco os outros metodos como create, update, delete?
	        'GET': self.GET,
	        'POST': self.POST
	    }
	    if request_method in methods:
	        methods[request_method](string)
	    else:
	        print "Unknown HTTP request method:", request_method, "\n"
	    print "Closing connection with client:", self.addr, "\n"
	    self.conn.close()

	def GET(self, string):
	    file_requested = string.split(' ') 		# Separa no espaco: "GET /file.html" -> ('GET','file.html',...)
	    file_requested = file_requested[1] 		# Pega o segundo elemento: 'file.html'
	    file_requested = file_requested.split('?')[0]  	# Ignora qualquer coisa depois do '?'

	    if (file_requested == '/'):  			# Caso o cliente nao especifique o arquivo,
	        file_requested = '/index.html' 		# a requisicao vai para o index.html

	    file_requested = self.www_dir + file_requested
	    print "Serving GET for web page [",file_requested,"]\n"

	 ## Load file content
	    try:
	        file_handler = open(file_requested,'rb')
	        response_content = file_handler.read()
	        file_handler.close()

	        response_headers = "Code: 200 OK\n"

	    except Exception as e: # Erro 404
	        print "File not found. Serving response code 404\n", e.strerror
	        response_content = "<html><body><p>Error 404: File not found</p></body></html>"
	    self.conn.send(response_content)

	def POST(self, string):
		request = string.split(' ')
		method = request[1].split('/')[1]
		args = request[len(request)-1].split('\n')
		data = args[len(args)-1]
		# print string
		# Separa no espaco e pega o segundo elemento: '/modulo'
		hashValue = self.getServer(data)
		rq = method+'?'+data
		# se for dele
		if hashValue == self.identifier:
			db = UserDB()
			response = db.processRequest(rq)
	  	# senao, manda request para outro router  
	 	else:
			string = self.serverMap[hashValue]+'/'+rq
			response = pythonclient.client(string)
		response = 'HTTP/1.0 200 OK\nContent-Type: text/html;charset=utf-8\n\n<html>'+response+'</html>\n'
		print response
  		self.conn.send(response)

		# calcula o valor  
	def hashFunction(self, key):
		return sum([ord(c) for c in key]) % self.serversNumber

		# obtem a key a partir da request
	def getKey(self, string):
		return string.split('&')[0].split('=')[1]
	  
		# obtem o idServer relacionado a key
	def getServer(self,string):
		return self.hashFunction(self.getKey(string))

def graceful_shutdown(sig, dummy):
    server.shutdown()

signal.signal(signal.SIGINT, graceful_shutdown)
server = PythonServer(8001, 1, 0, ['localhost'])
server.activate_server()
server.wait_for_connections()