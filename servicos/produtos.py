import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
import os
from database import get_connection


produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastro_produto')
def cadastro_produto():
    return render_template('cadastro_produto.html')


@produtos_bp.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco)
            VALUES (?, ?, ?)
        ''', (nome, descricao, preco))
        conn.commit()

    return redirect(url_for('produtos.cadastro_produto'))