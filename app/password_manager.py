from Cryptodome.Cipher import AES

def encrypt(key, plaintext):
    if type(plaintext) is str:
        plaintext = plaintext.encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce, tag, ciphertext

def write_encrypted_file(filename, key, text):
    nonce, tag, ciphertext = encrypt(key, text)
    with open(filename, 'wb') as f:
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

def decrypt(key, encrypted_text):
    nonce, tag, ciphertext = encrypted_text
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def read_encrypted_file(filename, key):
    with open(filename, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    encrypted_text = [nonce, tag, ciphertext]
    return decrypt(key, encrypted_text).decode('utf-8')