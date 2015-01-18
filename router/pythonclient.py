import httplib
import urllib 
from cgi import parse_qs, escape #metodos para quebrar url
from urllib2 import Request, urlopen, URLError, HTTPError

#A biblioteca urllib2 utiliza a biblioteca httplib, 
# que utiliza a biblioteca de socket. 
# configuracoes a nivel de sockets pode ser feitas como a insercao de um timeout de resposta do servidor: importando-se a biblioteca socket 

def client(url_req, routerId):
	httplib.HTTPConnection._http_vsn = 10
	httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

	try:
		if not url_req[:7]=="http://": #caso o protocolo nao tenha sido especificado na url
			url_req = "http://"+url_req
		
		url_new = url_req[:url_req.find('?')]
		dados_req = url_req[url_req.find('?')+1:] # separa dos dados da url
		data = parse_qs(dados_req)
		
		if data != {}:
			print dados_req
			req = Request(url_new,dados_req)
		else:
			req = Request(url_req)  #como nao tem o campo DATA, o metodo Request fara uma requisicao do tipo GET
			
		response = urlopen(req)
		
	except HTTPError as e:
		resposta = "O servidor nao pode completar a requisicao"
		resposta += "Codigo do erro: "+str(e.code)
		return resposta
		
	except URLError as e:
		resposta = "Servidor nao encontrado"
		resposta += "Motivo: "+str(e.reason)
		return resposta
		
	else:
		return response.read()