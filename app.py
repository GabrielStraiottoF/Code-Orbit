import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


from openai import AzureOpenAI

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")

client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version="2025-03-01-preview",
    azure_endpoint=AZURE_ENDPOINT
)

SYS_PROMPT = (
    "Você é uma consultora de beleza premium. "
    "Responda de forma curta, elegante e moderna, como um app de beleza. "
    
    "Nunca use listas numeradas ou estilo de artigo. "
    "Use no máximo 3 recomendações. "
    
    "Formato obrigatório:\n"
    "✨ Nome do produto\n"
    "Breve benefício (1 linha)\n"
    "Preço aproximado\n\n"
    
    "Use espaçamento entre produtos.\n"
    "Use poucos emojis (no máximo 1 por produto).\n"
    "Evite explicações longas.\n"
    
    "Finalize com uma dica curta e natural.\n"
)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                cpf TEXT NOT NULL UNIQUE,
                cep TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    cep = request.form.get('cep')
    senha_hash = generate_password_hash(request.form.get('senha'))

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, email, cpf, cep, senha) 
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, cpf, cep, senha_hash))
            conn.commit()
        return redirect(url_for('sucesso'))
    except sqlite3.IntegrityError:
        return "Erro: E-mail ou CPF já cadastrados.", 400

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("message") if data else None

    if not user_msg:
        return jsonify({"response": "Por favor, digite uma mensagem."}), 400

    try:
        response = client.responses.create(
            model=AZURE_DEPLOYMENT,
            input=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )

        resposta_ia = response.output_text

        return jsonify({"response": resposta_ia})

    except Exception as e:
        return jsonify({"response": f"Erro na IA: {str(e)}"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)