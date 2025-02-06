from flask import Flask
from threading import Thread
import os  # ← Añade esta importación

app = Flask('')

@app.route('/')
def index():
    return 'Hello from Flask!'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))  # Usa la variable PORT

def keep_alive():
    server = Thread(target=run)
    server.start()
