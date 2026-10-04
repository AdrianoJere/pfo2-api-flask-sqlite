"""Servidor API REST: registro y login de usuarios con contraseñas hasheadas,
persistencia en SQLite y un endpoint de bienvenida para las tareas."""
import sqlite3
import sys

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

DB_NAME = "usuarios.db"

app = Flask(__name__)


def inicializar_db():
    """Crea la base de datos y la tabla de usuarios si no existen."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        conexion.execute(
            """CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT NOT NULL UNIQUE,
                   contrasena_hash TEXT NOT NULL
               )"""
        )
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo acceder a la base de datos: {e}")
        sys.exit(1)


def obtener_usuario(usuario):
    """Busca un usuario por su nombre y devuelve su fila, o None si no existe."""
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    fila = conexion.execute(
        "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    conexion.close()
    return fila


def crear_usuario(usuario, contrasena_hash):
    """Inserta un nuevo usuario en la base de datos."""
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute(
        "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
        (usuario, contrasena_hash),
    )
    conexion.commit()
    conexion.close()


@app.route("/registro", methods=["POST"])
def registro():
    """Registra un usuario nuevo. Recibe {"usuario": "...", "contraseña": "..."}
    y guarda la contraseña hasheada, nunca en texto plano."""
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"status": "error", "message": "Se esperaba un JSON"}), 400

    # Acepta tanto "contraseña" (con ñ, como en la consigna) como "contrasena"
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify(
            {"status": "error", "message": "Faltan campos: usuario y contraseña"}
        ), 400

    if obtener_usuario(usuario):
        return jsonify(
            {"status": "error", "message": "El usuario ya existe"}
        ), 409

    # Hasheo de la contraseña: nunca se guarda en texto plano
    contrasena_hash = generate_password_hash(contrasena)

    try:
        crear_usuario(usuario, contrasena_hash)
    except sqlite3.Error as e:
        return jsonify(
            {"status": "error", "message": f"No se pudo guardar el usuario: {e}"}
        ), 500

    return jsonify(
        {"status": "success", "message": f"Usuario '{usuario}' registrado correctamente"}
    ), 201


@app.route("/login", methods=["POST"])
def login():
    """Verifica usuario y contraseña. Si son correctos, permite el acceso a las tareas."""
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"status": "error", "message": "Se esperaba un JSON"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify(
            {"status": "error", "message": "Faltan campos: usuario y contraseña"}
        ), 400

    fila = obtener_usuario(usuario)
    # check_password_hash compara la contraseña recibida contra el hash guardado
    if not fila or not check_password_hash(fila["contrasena_hash"], contrasena):
        return jsonify(
            {"status": "error", "message": "Usuario o contraseña incorrectos"}
        ), 401

    return jsonify(
        {
            "status": "success",
            "message": f"Bienvenido/a {usuario}. Ya podés acceder a /tareas",
        }
    )


@app.route("/tareas", methods=["GET"])
def tareas():
    """Devuelve un HTML de bienvenida al sistema de gestión de tareas."""
    html = """
    <html>
        <head><title>Gestión de Tareas</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 60px;">
            <h1>Bienvenido/a al Sistema de Gestión de Tareas</h1>
            <p>Iniciá sesión en /login para gestionar tus tareas.</p>
        </body>
    </html>
    """
    return html


@app.errorhandler(404)
def no_encontrado(e):
    """Maneja rutas inexistentes con un JSON claro en vez del HTML por defecto."""
    return jsonify({"status": "error", "message": "Endpoint no encontrado"}), 404


if __name__ == "__main__":
    inicializar_db()
    # debug=True solo para desarrollo local; se desactiva en un entorno real
    app.run(host="localhost", port=5000, debug=True)
