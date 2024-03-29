import socket 
import os 
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad  



def read_key_from_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

key = read_key_from_file('key') 
iv = get_random_bytes(16)

#--------------------------------------------------------------------------------------------------------------------------------------------#

HOST = '127.0.0.1' 
PORT = 16926
#--------------------------------------------------------------------------------------------------------------------------------------------#

def handle_exam(socket): 
    for i in range(4) : 
        prompt = socket.recv(1024).decode('utf-8')
        print(prompt)
        user_answer = input("Answer: ")
        padded_answer = pad(user_answer.encode(), AES.block_size)
        padded_answer_bytes = padded_answer
        cipher = AES.new(key, AES.MODE_CBC, iv)
        cipher_text = cipher.encrypt(padded_answer)
        socket.send(cipher_text)
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


