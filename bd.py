import psycopg2
from flask import jsonify

def getDBConnection():
    conn = psycopg2.connect(
        database = "ka",
        host = "localhost",
        user = "postgres",
        password = "postgres",
        port = "5432"
    )
    return conn

def getEmployee(username, password):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM funcionario WHERE nome = '{username}' AND senha = '{password}'")
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
        return jsonify({"message": "Employee not found"})

def createEmployee(newUsername, enterprise, position, newPassword): 
    
    conn = getDBConnection()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM empresas WHERE nome_empresa = '{enterprise}'")
    company = cur.fetchone()

    if company:
        cur.execute(
            f"INSERT INTO funcionario (id_empresa, nome, senha, cargo, nome_empresa) VALUES ('{company[0]}', '{newUsername}', '{newPassword}', '{position}', '{enterprise}') RETURNING id_user"
        )
        userId = cur.fetchone()[0]
        conn.commit() 
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()
        return jsonify({"message": "Company is not registered"})

    return jsonify({"message": "success", "id_user": userId})

def getEnterprise(username, password):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM empresas WHERE nome_empresa = '{username}' AND senha = '{password}'")
    company = cur.fetchone()
    cur.close()
    conn.close()

    if company:
        return jsonify({
            "message": "success",
            "id_empresa": company[0],
            "nome_empresa": company[1],
            "senha": company[2]
        })
    else:
        return jsonify({"message": 'Invalid Credentials'})

def createEnterprise(enterpriseName, password):

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO empresas (nome_empresa, senha) VALUES ('{enterpriseName}', '{password}') RETURNING id_empresa")
    companyId = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Enterprise create! Login now!", "id_empresa": companyId})

def checkFinalPoint(userId, data):
    conn = getDBConnection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT COUNT(*) FROM pontos WHERE id_user = '{userId}' AND DATE(hora_inicio) = '{data}'"
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    if count > 0:
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "false"})

def startPoint(userId, startTime):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO pontos (id_user, hora_inicio) VALUES ('{userId}', '{startTime}') RETURNING id_ponto")
    pointId = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success", "id_ponto": pointId})

def getDayPoint(userId, data):
    conn = getDBConnection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT * FROM pontos WHERE id_user = '{userId}' AND DATE(hora_inicio) = '{data}'"
    )
    points = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify({
        "id_ponto": points[0],
        "id_user": points[1],
        "hora_inicio": points[2]
    })

def finalPoint(pointId, finalTime):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE pontos SET hora_final = '{finalTime}' WHERE id_ponto = '{pointId}'"
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success"})

def getAllPoints(enterpriseId):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT p.id_ponto, p.id_user, p.hora_inicio, p.hora_final, f.nome
        FROM pontos p
        JOIN funcionario f ON p.id_user = f.id_user
        WHERE f.id_empresa = {enterpriseId}
        ORDER BY p.hora_inicio
    """)
    points = cur.fetchall()
    cur.close()
    conn.close()

    formatedPoints = [
        {
            "id_ponto": point[0],
            "id_user": point[1],
            "hora_inicio": point[2],
            "hora_final": point[3],
            "nome": point[4]
        }
        for point in points
    ]
    return jsonify(formatedPoints)

def deletePoint(pointId):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(
        f"DELETE FROM pontos WHERE id_ponto = '{pointId}'"
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success"})

def editPoint(pointId, startTime, finalTime):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE pontos SET hora_final = '{finalTime}', hora_inicio = '{startTime}' WHERE id_ponto = '{pointId}'"
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "success"})

# result = createEnterprise("creare", "creare")
# print(result)