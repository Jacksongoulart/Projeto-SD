import pythonserver
import pythonclient
import sys
sys.path.append('../banco/') from UserDB import *
class PythonRouter:

  def __init__(self, port)
    """ Constructor """
    self.routersNumber = 3
    self.identifier = 1
    self.server = pythonserver.PythonServer(port, dir, self.identifier)
   
  # calcula o valor  
  def hashFuncion(self, key)
    return sum([ord(c) for c in key]) % self.serversNumber
  
  # obtem a key a partir da request
  def getKey(self, string)
    return string.split('&')[0].split('=')[1]
  
  # obtem o idServer relacionado a key
  def getServer(self,string)
    return hashFuncion(self, getKey(self, string))
  
  
  # decide de qual router é a request 
  def callServer(self, string)
    hashValue = getServer(string)
    # se for dele
    if (hashValue == self.identifier):
      userDB = UserDB()
      userDB.processRequest(string)
    # senao, manda request para outro router  
    else:
      pythonclient.client(string,hashValue)
    
      
      