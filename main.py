from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Aktifkan CORS untuk mengizinkan akses dari semua domain
CORS(app)

# Route untuk halaman utama API
@app.route('/')
def welcome():
    return jsonify({"message": "Selamat Datang di Vigenere Chipper Generator"}), 200

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        data = request.get_json()

        # Validasi input
        if 'plaintext' not in data or 'key' not in data:
            return jsonify({'error': 'Missing "plaintext" or "key"'}), 400

        plaintext = data['plaintext']
        key = data['key']

        if not plaintext or not key:
            return jsonify({'error': 'Both "plaintext" and "key" must be provided'}), 400

        encrypted_text = vigenere_encrypt(plaintext, key)
        return jsonify({'encrypted': encrypted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        data = request.get_json()

        # Validasi input
        if 'ciphertext' not in data or 'key' not in data:
            return jsonify({'error': 'Missing "ciphertext" or "key"'}), 400

        ciphertext = data['ciphertext']
        key = data['key']

        if not ciphertext or not key:
            return jsonify({'error': 'Both "ciphertext" and "key" must be provided'}), 400

        decrypted_text = vigenere_decrypt(ciphertext, key)
        return jsonify({'decrypted': decrypted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
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

if __name__ == '__main__':
    app.run(debug=True)
