from banco import *
import json

#campos:
#0: email
#1: senha
#2: nome
#3: sexo
#4: dataNascimento

class UserDB:

	ARQUIVO = "usuario.txt"

	fields = {
		'email': 0,
		'senha': 1,
		'campos': 1,
		'nome':2,
		'sexo': 3,
		'dataNascimento': 4
	}

	def __init__(self):
		self.db = Banco(20, self.ARQUIVO)

	def processRequest(self, request):
		dataArray = ['!','!','!','!','!']
		req = request.split('?')
		op = req[0]
		data = req[1].split('&')
		for field in data:
			fieldInfo = field.split('=')
			if fieldInfo[0] in self.fields:	
				dataArray[self.fields[fieldInfo[0]]] = fieldInfo[1]

		operacoes = {
	        'addUser': self.addUser,
	        'deleteUser': self.deleteUser,
	        'loginUser': self.loginUser,
	        'readUser': self.readUser,
	        'updateUser': self.updateUser
	    }

		if op in operacoes:
			return operacoes[op](dataArray[0], dataArray[1:])
		return "Erro"

	def addUser(self, chave, dadosReq):
		r1, r2 = self.db.read(chave)
		if not r1:
			self.db.create(chave, dadosReq)
			return "Ok"
		else:
			return "Erro"

	def deleteUser(self, chave, dadosReq):
		r1, r2 = self.db.read(chave)
		if (not r1) or r2[1] != dadosReq[0]:
			return "Erro"
		else:
			self.db.delete(chave)
			return "Ok"

	def loginUser(self, chave, dadosReq):
		r1, r2 = self.db.read(chave)
		if (not r1) or (r2[1] != dadosReq[0]):
			return "Erro"
		else:
			return "Ok"

	def readUser(self, chave, dadosReq):
		r1, r2 = self.db.read(chave)
		if not r1:
			return "Erro"
		else:
			dataDict = {}
			fields = dadosReq[0].split('|')
			for field in fields:
				if field in self.fields:
					dataDict[field] = r2[self.fields[field]]
		return json.dumps(dataDict)


	def updateUser(self, chave, dadosReq):
		if self.db.update(chave, dadosReq):
			return "Ok"
		return "Erro"


# db = UserDB()

# addReq = "addUser?email=email1@email&senha=senha1&nome=nome1&sexo=M&dataNascimento=10/10/10"
# readReq = "readUser?email=email1@email&campos=nome|email"
# delReq = "deleteUser?email=email1@email&senha=senha1"
# updateReq = "updateUser?email=email1@email&sexo=F"
# print db.processRequest(updateReq)