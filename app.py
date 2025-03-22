from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('livros.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Bem-vindo à API de Livros! Use as rotas /livros para ver os livros e /doar para adicionar um novo livro."

# Usar o 127.0.0.1:5000/doar
@app.route('/doar', methods=['POST'])
def cadastrar_livro():
    data = request.get_json()
    
    titulo = data.get('titulo')
    categoria = data.get('categoria')
    autor = data.get('autor')
    image_url = data.get('image_url')
    
    if not titulo or not categoria or not autor or not image_url:
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criar a tabela caso n exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIVROS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES (?, ?, ?, ?)
    ''', (titulo, categoria, autor, image_url))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Livro doado com sucesso!'}), 201

# Rota para listar os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM LIVROS')
    livros = cursor.fetchall()
    conn.close()

    livros_list = []
    for livro in livros:
        livros_list.append({
            'id': livro['id'],
            'titulo': livro['titulo'],
            'categoria': livro['categoria'],
            'autor': livro['autor'],
            'image_url': livro['image_url']
        })

    return jsonify(livros_list)

if __name__ == '__main__':
    app.run(debug=True)
