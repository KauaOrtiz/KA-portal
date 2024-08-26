from flask import Flask, json, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/employee", methods=['GET', 'POST'])
def loginEmployee():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username == 'admin' and password == 'password':
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
                sucess = "User create! Login now!"
                return render_template('login_employee.html', sucess=sucess)
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
            if company == 'admin' and password == 'password':
                return redirect(url_for('dashboardEnterprise'))
            else:
                error = 'Invalid Credentials'
                return render_template('login_enterprise.html', error=error)
        elif 'new-company' in request.form:
            new_company = request.form['new-company']
            new_password = request.form['new-password']
            confirm_password = request.form['confirm-password']
            if new_password == confirm_password:
                sucess = "Enterprise create! Login now!"
                return render_template('login_enterprise.html', sucess=sucess)
            else:
                error = "Passwords don't match"
                return render_template('login_enterprise.html', error=error)
    return render_template('login_enterprise.html')

@app.route("/dashboard/employee")
def dashboardEmployee():
    return render_template("dashboard_enterprise.html")

@app.route("/dashboard/enterprise")
def dashboardEnterprise():
    return render_template("dashboard_enterprise.html")


if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0') 