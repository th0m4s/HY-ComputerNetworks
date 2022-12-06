from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("0.0.0.0", serverPort))
serverSocket.listen()
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    print(sentence.decode("utf-8"))
    connectionSocket.close()
