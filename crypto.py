from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def read_key_from_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


key_file_path = 'key'


key = read_key_from_file(key_file_path)

# Initialization Vector (IV) generation
iv = get_random_bytes(16)

# Data to be encrypted
data = input("Please enter a message: ") 
data = bytes(data, 'utf-8')
# Padding the data
padded_data = pad(data, AES.block_size)

# AES encryption
cipher = AES.new(key, AES.MODE_CBC, iv)
cipher_text = cipher.encrypt(padded_data)

# AES decryption
decipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_padded_data = decipher.decrypt(cipher_text)

# Remove padding
plain_text = unpad(decrypted_padded_data, AES.block_size)

print("Original data:", str(data))
print("Decrypted data:", plain_text)
