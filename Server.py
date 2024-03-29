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

MESSAGES = ["Enter the server IP or name: ", "Welcome to examination System\nPlease enter your name: "]
OPERATORS = ["+", "-", "*"]
HOST = '127.0.0.1' 
PORT = 13002

def handle_client(conn):
    total = 0
    conn.send(MESSAGES[0].encode('utf-8'))
    HOSTNAME = conn.recv(1024).decode('utf-8')  # Can use later
    print(HOSTNAME)
    conn.send(MESSAGES[1].encode('utf-8'))
    studentName = conn.recv(1024).decode('utf-8')
    loop_val = True
    while loop_val:
        for i in range(4):
            score = test(conn, i)
            total += score
        loop_choice = f"You achieved a score of {total}/4\nWould you like to try again? (y/n): "
        conn.send(loop_choice.encode('utf-8'))
        choice = conn.recv(1024).decode('utf-8')
        if choice != 'y':
            loop_val = False
    conn.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("The server is ready to accept connections...")
    while True:
        conn, addr = server_socket.accept()
        pid = os.fork()
        if pid == 0:  # Child process
            server_socket.close()  # Close child's copy of server socket
            handle_client(conn)
            os._exit(0)  # Exit child process
        else:  # Parent process
            conn.close()  # Close parent's copy of client socket

def test(conn, i):
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

def equation(qINDEX: int, conn) -> int:
    operands = (random.randint(0, 100), random.randint(0, 100))
    operator = OPERATORS[random.randint(0, 2)]
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

