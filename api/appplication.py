from flask import Flask, request
from flask_cors import CORS

# from ..algo.task2 import Cryptography

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello"


@app.route("/symmetric/aes/encrypt", methods=["POST"])
def aes_encrypt():
    key_size = request.json.get("key_size")
    mode = request.json.get("block_cipher_mode")
    plaintext = request.json.get("plaintext")

    if not all([key_size, mode, plaintext]):
        return {"error": "Missing required fields"}, 400

    # crypto = Cryptography("aes", key_size, mode)
    # ciphertext = crypto.strategy.encrypt(plaintext.encode())

    return {"ciphertext": "Hello"}
