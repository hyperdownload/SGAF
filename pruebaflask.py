from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route("/respuesta", methods= ["POST"])
def respuesta():
    nombre = request.form.get("email")
    edad = request.form.get("password")
    return render_template("respuesta.html",nombre=nombre, edad=edad)

if __name__ == '__main__':
    app.run(debug=True)
