import os

class Banco:

	def __init__(self, X, filename):
		self.file = filename
		self.max_size = X

	def create(self, k, v):
		arq = open(self.file, "a")
		arq.write(self.__arrayToText(k,v))
		arq.close()

	def read(self, k):
		arq = open(self.file, "r")
		key = ""
		while key != k:
			line = arq.readline()
			key = line.split('|')[0]
			if key == "":
				arq.close()
				return False, []
		arq.close()
		v = self.__textToArray(line)
		return True, v

	def update(self, k, v):
		tempFile = "tempFile.txt"
		tempArq = open(tempFile, "w")
		arq = open(self.file, "r")
		line = self.__copyUntil(k, tempArq, arq)
		if line == "":
			arq.close()
			tempArq.close()
			os.remove(tempFile)
			return False

		reg = self.__textToArray(line)
		v2 = reg[1:]

		for i in range(len(v)):
			if v[i] != "!":
				v2[i] = v[i]
		tempArq.write(self.__arrayToText(k, v2))

		self.__copyToFile(arq, tempArq)
		arq.close()
		tempArq.close()
		os.rename(tempFile, self.file)
		return True

	def delete(self, k):
		tempFile = "tempFile.txt"
		tempArq = open(tempFile, "w")
		arq = open(self.file, "r")
		line = self.__copyUntil(k, tempArq, arq)

		if line == "":
			arq.close()
			tempArq.close()
			os.remove(tempFile)
			return False

		self.__copyToFile(arq, tempArq)
		arq.close()
		tempArq.close()
		os.rename(tempFile, self.file)
		return True

	def __copyUntil(self, k, tempArq, arq):
		while True:
			arqAux = arq
			line = arq.readline()
			key = line.split('|')[0]
			if key == "":
				return ""
			elif key == k:
				break
			tempArq.write(line)
		return line

	def __copyToFile(self, arq1, arq2):
		line = "a"
		while line != "":
			line = arq1.readline()
			arq2.write(line)

	def __arrayToText(self, k, v):
		word = k
		for value in v:
			word = word + "|" + value
		word = word + '\n'
		return word

	def __textToArray(self, v):
		v = v.split('\n')[0] # remove o \n
		return v.split('|')