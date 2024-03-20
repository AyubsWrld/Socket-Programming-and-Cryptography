import socket 
import os 
from Crypto.Cipher import AES

#--------------------------------------------------------------------------------------------------------------------------------------------#

HOST = '127.0.0.1' 
PORT = 13000

#--------------------------------------------------------------------------------------------------------------------------------------------#

def handle_exam(socket): 
    for i in range(4) : 
        prompt = socket.recv(1024).decode('utf-8')
        print(prompt)
        user_answer = input("Answer: ")
        socket.send(user_answer.encode('utf-8'))  
    results = socket.recv(1024).decode('utf-8')
    print(results)

#--------------------------------------------------------------------------------------------------------------------------------------------#

def client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    IPMESSAGE = client_socket.recv(1024).decode('utf-8')
    print(IPMESSAGE , end = '')
    HOSTNAME = input('')
    client_socket.send(HOSTNAME.encode('utf-8'))
    CONNECTIONMESSAGE = client_socket.recv(1024).decode('utf-8')
    print(CONNECTIONMESSAGE, end = '')
    name = input()
    client_socket.send(name.encode('utf-8'))
    while True:
        handle_exam(client_socket)
        loopChoice = input()
        client_socket.send(loopChoice.encode('utf-8'))
        if loopChoice != 'y' : 
            break
    client_socket.close()

#--------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    client()


