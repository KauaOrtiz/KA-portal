import psycopg2
from flask import jsonify

def get_db_connection():
    conn = psycopg2.connect(
        database = "ka",
        host = "localhost",
        user = "postgres",
        password = "postgres",
        port = "5432"
    )
    return conn

def busca_funcionario(username, senha):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM funcionario WHERE nome = '{username}' AND senha = '{senha}'")
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({
            "message": "success",
            "id_user": user[0],
            "id_empresa": user[1],
            "nome": user[2],
            "cargo": user[4],
            "nome_empresa": user[5]
        })
    else:
        return jsonify({"message": "Usuário não encontrado"})

def create_funcionario(new_username, enterprise, position, new_password): 
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM empresas WHERE nome_empresa = '{enterprise}'")
    empresa = cur.fetchone()

    if empresa:
        cur.execute(
            f"INSERT INTO funcionario (id_empresa, nome, senha, cargo, nome_empresa) VALUES ('{empresa[0]}', '{new_username}', '{new_password}', '{position}', '{enterprise}') RETURNING id_user"
        )
        id_user = cur.fetchone()[0]
        conn.commit() 
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()
        return jsonify({"message": "Empresa não cadastrada"})

    return jsonify({"message": "success", "id_user": id_user})

def buscar_empresa(username, senha):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM empresas WHERE nome_empresa = '{username}' AND senha = '{senha}'")
    empresa = cur.fetchone()
    cur.close()
    conn.close()

    if empresa:
        return jsonify({
            "message": "success",
            "id_empresa": empresa[0],
            "nome_empresa": empresa[1],
            "senha": empresa[2]
        })
    else:
        return jsonify({"message": 'Invalid Credentials'})

def create_empresa(nome_empresa, senha):

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO empresas (nome_empresa, senha) VALUES ('{nome_empresa}', '{senha}') RETURNING id_empresa")
    id_empresa = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Enterprise create! Login now!", "id_empresa": id_empresa})

def ver_se_eh_ponto_saida(id_user, data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT COUNT(*) FROM pontos WHERE id_user = '{id_user}' AND DATE(hora_inicio) = '{data}'"
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    if count > 0:
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "false"})

def bater_ponto_entrada(id_user, hora_inicio):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO pontos (id_user, hora_inicio) VALUES ('{id_user}', '{hora_inicio}') RETURNING id_ponto")
    id_ponto = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success", "id_ponto": id_ponto})

def buscar_ponto_dia(id_user, data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT * FROM pontos WHERE id_user = '{id_user}' AND DATE(hora_inicio) = '{data}'"
    )
    pontos = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify({
        "id_ponto": pontos[0],
        "id_user": pontos[1],
        "hora_inicio": pontos[2]
    })

def bater_ponto_saida(id_ponto, data_final):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE pontos SET hora_final = '{data_final}' WHERE id_ponto = '{id_ponto}'"
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success"})

def buscar_todos_pontos(id_empresa):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT p.id_ponto, p.id_user, p.hora_inicio, p.hora_final, f.nome
        FROM pontos p
        JOIN funcionario f ON p.id_user = f.id_user
        WHERE f.id_empresa = {id_empresa}
        ORDER BY p.hora_inicio
    """)
    pontos = cur.fetchall()
    cur.close()
    conn.close()

    pontos_formatados = [
        {
            "id_ponto": ponto[0],
            "id_user": ponto[1],
            "hora_inicio": ponto[2],
            "hora_final": ponto[3],
            "nome": ponto[4]
        }
        for ponto in pontos
    ]
    return jsonify(pontos_formatados)

def apagar_ponto():
    pass

def editar_ponto(id_ponto, hora_inicio, hora_final):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE pontos SET hora_final = '{hora_final}', hora_inicio = '{hora_inicio}' WHERE id_ponto = '{id_ponto}'"
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success"})

# result = create_empresa("creare", "creare")
# print(result)