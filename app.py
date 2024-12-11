from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import pusher

# Conexión a la base de datos MySQL
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1767934',
    key='ffa9ea426828188c22c1',
    secret='628348e447718a9eec1f',
    cluster='us2',
    ssl=True
)

@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()
    return render_template("app.html", usuarios=registros)

# Ruta para guardar un nuevo usuario
@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    usuario = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    val = (usuario, contrasena)
    cursor.execute(sql, val)

    con.commit()

    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
        "usuario": usuario,
        "contrasena": contrasena
    })

    return redirect(url_for("index"))

# Ruta para actualizar un usuario
@app.route("/usuarios/actualizar/<int:id>", methods=["POST"])
def usuarios_actualizar(id):
    usuario = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s"
    val = (usuario, contrasena, id)
    cursor.execute(sql, val)

    con.commit()

    return redirect(url_for("index"))

# Ruta para eliminar un usuario
@app.route("/usuarios/eliminar/<int:id>", methods=["POST"])
def usuarios_eliminar(id):
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id,)
    cursor.execute(sql, val)

    con.commit()
