class Banco:

	ARQUIVO = "usuario.txt"

	def __init__(self, X):
		self.max_size = X

	def create(self, k, v):
		arq = open(self.ARQUIVO, "a")
		arq.write(self.__formatText(k,v))

	def read(self, k):
		return

	def update(self, k,v):
		return

	def delete(self, k):
		return

	def __formatText(self, k, v):
		word = k + "=|="
		for value in v:
			word = word + "|" + value
		word = word + '\n'
		return word

db = Banco(20)
dados = {"t1":"teste1", "t2":"teste2"}
db.create("data3", dados)