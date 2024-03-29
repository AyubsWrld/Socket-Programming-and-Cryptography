import socket 
import random 
import os 
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

def read_key_from_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

key_file_path = 'key'
key = read_key_from_file(key_file_path)
iv = get_random_bytes(16)
MESSAGES = ["Enter the server IP or name: ", "Welcome to the examination System\nPlease enter your name: "]
OPERATORS = ["+", "-", "*"]
HOST = '127.0.0.1' 
PORT = 16952

def server(): 
    index = 1 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print("The server is ready to accept connections...")
    
    while index < 10: 
        child_pid = os.fork()
        if child_pid == 0: 
            conn, addr = server_socket.accept()
            print(f"Connection successful with client {index}")
            handle_client(conn)
            os._exit(0)
            conn.close()
            break
            
        else:
            index += 1

def handle_client(conn):
    conn.send(MESSAGES[0].encode('utf-8'))
    HOSTNAME = conn.recv(1024).decode('utf-8') 
    conn.send(MESSAGES[1].encode('utf-8'))
    studentName = conn.recv(1024).decode('utf-8')
    total = 0
    loopVal = True
    while loopVal: 
        for i in range(4): 
            score = test(conn, i)
            total += score
        
        loopChoice = f"You achieved a score of {total}/4\nWould you like to try again? (y/n): "
        conn.send(loopChoice.encode('utf-8'))
        choice = conn.recv(1024).decode('utf-8')
        if choice != 'y': 
            conn.close()
            loopVal = False
            break

def test(conn, i):
    score = 0
    result = equation(i, conn)
    user_answer = conn.recv(1024)
    print(f"Encrypted message received: {user_answer}")
    decipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_data = decipher.decrypt(user_answer)
    plain_text = unpad(decrypted_padded_data, AES.block_size)
    print(f"Decrypted message: {plain_text.decode('utf-8')}")
    score += 1 
    return score

def equation(qINDEX : int , conn) -> int : 
    operands = (random.randint(0,100) , random.randint(0,100)) 
    operator = OPERATORS[random.randint(0,2)]
    message = f"Question number {qINDEX + 1}: {operands[0]} {operator} {operands[1]}"
    conn.send(message.encode('utf-8'))
    if operator == '+': 
        answer = operands[0] + operands[1]
    elif operator == '-':
        answer = operands[0] - operands[1]
    else:
        answer = operands[0] * operands[1]
    return int(answer)

if __name__ == "__main__":
    server()
