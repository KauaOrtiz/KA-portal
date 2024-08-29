from flask import Flask, json, session, render_template, request, redirect, url_for

from datetime import datetime, date

from bd import (
    createEnterprise, 
    getEnterprise, 
    createEmployee, 
    getEmployee,
    checkFinalPoint,
    startPoint,
    getAllPoints,
    finalPoint,
    getDayPoint,
    deletePoint,
    editPoint
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

            result = getEmployee(username, password)
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
                result = createEmployee(new_username, enterprise, position, new_password)
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

            result = getEnterprise(company, password)
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
                result = createEnterprise(new_company, new_password)
                data = result.json
                state = data["message"]
                return render_template('login_enterprise.html', state=state)
            
            else:
                state = "Passwords don't match"
                return render_template('login_enterprise.html', state=state)
            
    return render_template('login_enterprise.html')
    
@app.route("/dashboard/employee", methods=['GET', 'POST'])
def dashboardEmployee():
    if request.method == 'POST':
        result2 = checkFinalPoint(session.get('id_user'), date.today())
        data2 = result2.json

        if data2["message"] == "success":
            ponto = getDayPoint(session.get('id_user'), date.today())
            dados = ponto.json
            result4 = finalPoint(dados['id_ponto'], getDatetime())
            data4 = result4.json
            if data4['message'] == "success":
                return render_template("dashboard_employee.html", sucess="Exit Point")
        else:
            result = startPoint(session.get('id_user'), getDatetime())
            print(result.json)
            return render_template("dashboard_employee.html", sucess="Entry Point")
    else:
        return render_template("dashboard_employee.html")

@app.route("/dashboard/enterprise", methods=['GET', 'POST'])
def dashboardEnterprise():
    if request.method == "GET":
        result = getAllPoints(session.get('id_empresa'))
        pontos = result.json
        return render_template("dashboard_enterprise.html", sucessAll=pontos)

    elif request.method == "POST":
        if 'hora_inicio' in request.form:
            id_ponto = request.form["id_ponto"]
            hora_inicio = request.form["hora_inicio"]
            hora_final = request.form["hora_final"]

            hora_inicio = datetime.strptime(hora_inicio, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')
            hora_final = datetime.strptime(hora_final, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')

            result = getAllPoints(session.get('id_empresa'))
            pontos = result.json

            for ponto in pontos:
                if ponto["id_ponto"] == int(id_ponto):
                    result = editPoint(int(id_ponto), hora_inicio, hora_final)
                    data = result.json
                    if data['message'] == 'success':
                        return render_template("dashboard_enterprise.html", sucessEdit="Point changed successfully")
        
        elif "id_ponto_delete" in request.form:
            id_ponto = request.form["id_ponto_delete"]
            result = getAllPoints(session.get('id_empresa'))
            pontos = result.json
            for ponto in pontos:
                if ponto["id_ponto"] == int(id_ponto):
                    result = deletePoint(int(id_ponto))
                    data = result.json
                    if data['message'] == 'success':
                        return render_template("dashboard_enterprise.html", sucessDelete="Point deleted successfully")

    return render_template("dashboard_enterprise.html", error="Point not found")


def getDatetime():
    agora = datetime.now()
    return agora

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')