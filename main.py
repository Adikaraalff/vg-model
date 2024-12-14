from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Fungsi untuk mengenkripsi pesan dengan Vigenère Cipher
def vigenere_encrypt(plaintext, key):
    ciphertext = []
    key = key.upper()
    plaintext = plaintext.upper()
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext.append(encrypted_char)
            key_index = (key_index + 1) % len(key)
        else:
            ciphertext.append(char)

    return ''.join(ciphertext)

# Fungsi untuk mendekripsi pesan dengan Vigenère Cipher
def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key = key.upper()
    ciphertext = ciphertext.upper()
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_index = (key_index + 1) % len(key)
        else:
            plaintext.append(char)

    return ''.join(plaintext)

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.get_json()
    plaintext = data['plaintext']
    key = data['key']
    encrypted_text = vigenere_encrypt(plaintext, key)
    return jsonify({'encrypted': encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    data = request.get_json()
    ciphertext = data['ciphertext']
    key = data['key']
    decrypted_text = vigenere_decrypt(ciphertext, key)
    return jsonify({'decrypted': decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
