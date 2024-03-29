import socket 
import random 
import os 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
def read_key_from_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

key_file_path = 'key'
key = read_key_from_file(key_file_path)

#--------------------------------------------------------------------------------------------------------------------------------------------#

MESSAGES = ["Enter the server IP or name: " , "Welcome to examination System\nPlease enter your name: "]
OPERATORS = ["+" , "-" , "*"]
HOST = '127.0.0.1' 
PORT = 13000

#--------------------------------------------------------------------------------------------------------------------------------------------#

def server(): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen()
    print("The server is ready to accpet connections...")
    while True : 
        total = 0 
        conn, addr = server_socket.accept()
        conn.send(MESSAGES[0].encode('utf-8'))
        HOSTNAME = conn.recv(1024).decode('utf-8') #Can use later
        print(HOSTNAME)
        conn.send(MESSAGES[1].encode('utf-8'))
        studentName = conn.recv(1024).decode('utf-8')
        loopVal = True
        while loopVal : 
            for i in range(4) : 
                score = test(conn, i )
                total += score
            loopChoice = f"You achieved a score of {total}/4\nWould you like to try again? (y/n): "
            conn.send(loopChoice.encode('utf-8'))
            choice = conn.recv(1024).decode('utf-8')
            if choice != 'y' : 
                loopVal = False
        break

#--------------------------------------------------------------------------------------------------------------------------------------------#

def test(conn,i):
    score = 0
    result = equation(i, conn)
    cipher_text = conn.recv(1024)

    decipher = AES.new(key, AES.MODE_CBC, cipher_text[:AES.block_size])
    decrypted_data = decipher.decrypt(cipher_text[AES.block_size:])
    unpadded_data = unpad(decrypted_data, AES.block_size)
    print(f"Encrypted message received: {cipher_text}")
    test = str(unpadded_data)
    answer = int(test[2:-1])
    print(f"Decrypted message received: {answer}")
    if int(answer) == int(result): 
        score += 1 
    return score

#--------------------------------------------------------------------------------------------------------------------------------------------#


def equation(qINDEX : int , conn) -> int : 
    operands = (random.randint(0,100) , random.randint(0,100)) 
    operator = OPERATORS[random.randint(0,2)]
    message = f"Question number {qINDEX + 1}: {operands[0]} {operator} {operands[1]}"
    conn.send(message.encode('utf-8'))
    if operator == '+' : 
        answer = operands[0] + operands[1]
    elif operator == '-':
        answer = operands[0] - operands[1]
    else:
        answer = operands[0] * operands[1]
    # print(f"Answer: {answer}")
    return int(answer)

    
#--------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    server()

