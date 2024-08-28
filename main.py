from flask import Flask, json, session, render_template, request, redirect, url_for

from datetime import datetime, date

from bd import (
    create_empresa, 
    buscar_empresa, 
    create_funcionario, 
    busca_funcionario,
    ver_se_eh_ponto_saida,
    bater_ponto_entrada,
    buscar_todos_pontos,
    bater_ponto_saida,
    buscar_ponto_dia,
    apagar_ponto,
    editar_ponto
)

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/employee", methods=['GET', 'POST'])
def loginEmployee():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']

            result = busca_funcionario(username, password)
            data = result.json

            if username == 'admin' and password == 'password':
                return redirect(url_for('dashboardEmployee'))
            
            elif data['message'] == "success":
                print("Funcionario: ", data)
                session['id_user'] = data['id_user']
                return redirect(url_for('dashboardEmployee'))

            else:
                error = 'Invalid Credentials'
                return render_template('login_employee.html', error=error)
            
        elif 'new-username' in request.form:
            new_username = request.form['new-username']
            enterprise = request.form['enterprise']
            position = request.form['position']
            new_password = request.form['new-password']
            confirm_password = request.form['confirm-password']

            if new_password == confirm_password:
                result = create_funcionario(new_username, enterprise, position, new_password)
                data = result.json

                if data['message'] == "success":
                    sucess = "User create! Login now!"
                    return render_template('login_employee.html', sucess=sucess)
                else:
                    error = data["message"]
                    return render_template('login_employee.html', error=error)
            else:
                error = "Passwords don't match"
                return render_template('login_employee.html', error=error)

    return render_template('login_employee.html')

@app.route("/login/enterprise", methods=['GET', 'POST'])
def loginEnterprise():
    if request.method == 'POST':
        if 'company' in request.form:
            company = request.form['company']
            password = request.form['password']

            result = buscar_empresa(company, password)
            data = result.json
            
            if company == 'admin' and password == 'password':
                return redirect(url_for('dashboardEnterprise'))
            
            elif data['message'] == "success":
                session['id_empresa'] = data['id_empresa']
                print("Empresa: ", data)
                return redirect(url_for('dashboardEnterprise'))

            else:
                error = data["message"]
                return render_template('login_enterprise.html', error=error)
            
        elif 'new-company' in request.form:
            new_company = request.form['new-company']
            new_password = request.form['new-password']
            confirm_password = request.form['confirm-password']

            if new_password == confirm_password:
                result = create_empresa(new_company, new_password)
                data = result.json
                sucess = data["message"]
                return render_template('login_enterprise.html', sucess=sucess)
            
            else:
                error = "Passwords don't match"
                return render_template('login_enterprise.html', error=error)
            
    return render_template('login_enterprise.html')

def obter_data_hora_atual():
    agora = datetime.now()  # Obtém a data e hora atuais
    return agora

@app.route("/dashboard/employee", methods=['GET', 'POST'])
def dashboardEmployee():
    if request.method == 'POST':
        result2 = ver_se_eh_ponto_saida(session.get('id_user'), date.today())
        data2 = result2.json

        if data2["message"] == "success":
            ponto = buscar_ponto_dia(session.get('id_user'), date.today())
            dados = ponto.json
            result4 = bater_ponto_saida(dados['id_ponto'], obter_data_hora_atual())
            data4 = result4.json
            if data4['message'] == "success":
                return render_template("dashboard_employee.html", sucess="Ponto de Saída")
        else:
            result = bater_ponto_entrada(session.get('id_user'), obter_data_hora_atual())
            print(result.json)
            return render_template("dashboard_employee.html", sucess="Ponto de Entrada")
    else:
        return render_template("dashboard_employee.html")


@app.route("/dashboard/enterprise", methods=['GET', 'POST'])
def dashboardEnterprise():
    if request.method == "GET":
        result = buscar_todos_pontos(session.get('id_empresa'))
        pontos = result.json
        print(pontos)
        return render_template("dashboard_enterprise.html", sucess=pontos)

    elif request.method == "POST":
        if 'hora_inicio' in request.form: 
            id_ponto = request.form["id_ponto"]
            hora_final = request.form["hora_final"]
            hora_inicio = request.form["hora_inicio"]
            result = buscar_todos_pontos(session.get('id_empresa'))
            pontos = result.json
            print(pontos, "akosjhbcisdbclisdcbidcb")
            for ponto in pontos:
                if ponto["id_ponto"] == int(id_ponto):
                    print(ponto)
                    result = editar_ponto(int(id_ponto), hora_inicio, hora_final)
                    print("result")
                    return render_template("dashboard_enterprise.html", sucess=result.json)
                else:
                    return render_template("dashboard_enterprise.html", error="Ponto não encontrado")
    
    return render_template("dashboard_enterprise.html", error="Ponto não encontrado")

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0') 