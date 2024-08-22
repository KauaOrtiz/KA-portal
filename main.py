from flask import Flask, json, render_template, request

app = Flask(__name__)
with open("alunos.json", "r") as f:
    alunos = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/employee")
def loginEmployee():
    return render_template("login_employee.html")

@app.route("/login/enterprise")
def loginEnterprise():
    return render_template("login_enterprise.html")

@app.route("/dashboard/employee")
def dashboardEmployee():
    return render_template("dashboard_enterprise.html")

@app.route("/dashboard/enterprise")
def dashboardEnterprise():
    return render_template("dashboard_enterprise.html")


if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0') 