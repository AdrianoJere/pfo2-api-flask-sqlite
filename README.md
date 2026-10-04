# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

API REST hecha con **Flask** que permite registrar usuarios con contraseñas
hasheadas, iniciar sesión, y acceder a un endpoint de bienvenida al sistema
de tareas. Los datos se guardan en **SQLite**. Incluye un cliente de consola
que interactúa con la API usando la librería `requests`.

## Archivos

- `servidor.py`: API Flask con los endpoints `/registro`, `/login` y `/tareas`.
- `cliente.py`: cliente de consola que consume la API.
- `requirements.txt`: dependencias del proyecto.
- `docs/index.html`: página publicada con GitHub Pages (ver la nota al final).

## Requisitos

- Python 3.
- Las librerías listadas en `requirements.txt` (Flask y requests).

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

1. En una terminal, iniciar el servidor:
   ```bash
   python servidor.py
   ```
   Queda escuchando en `http://localhost:5000`.

2. En otra terminal, ejecutar el cliente:
   ```bash
   python cliente.py
   ```
   Muestra un menú con las opciones: registrarse, iniciar sesión, ver tareas
   y salir.

## Endpoints

| Método | Ruta        | Descripción                                                |
|--------|-------------|-------------------------------------------------------------|
| POST   | `/registro` | Crea un usuario nuevo. Recibe `{"usuario", "contraseña"}`   |
| POST   | `/login`    | Verifica las credenciales y da acceso a las tareas          |
| GET    | `/tareas`   | Devuelve un HTML de bienvenida                               |

## Cómo probarlo

### Con el cliente de consola
Seguir el menú: **1** para registrarse, **2** para iniciar sesión con esos
mismos datos, y **3** para ver la respuesta de `/tareas`. Si se elige **3**
sin haber iniciado sesión antes, el cliente lo avisa y no deja continuar.

### Con curl (opcional, probando la API directamente)
```bash
# Registro
curl -X POST http://localhost:5000/registro -H "Content-Type: application/json" -d "{\"usuario\":\"adriano\",\"contraseña\":\"1234\"}"

# Login
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"usuario\":\"adriano\",\"contraseña\":\"1234\"}"

# Tareas
curl http://localhost:5000/tareas
```

### Verificar que la contraseña se guarda hasheada
```bash
python -c "import sqlite3; print(sqlite3.connect('usuarios.db').execute('select * from usuarios').fetchall())"
```
Debería verse una cadena larga tipo `scrypt:...`, nunca la contraseña en
texto plano.

## Documentación completa

Las capturas de las pruebas realizadas y las respuestas conceptuales
(por qué hashear contraseñas, ventajas de SQLite) están publicadas en
GitHub Pages: **https://adrianojere.github.io/pfo2-api-flask-sqlite/**

(También se pueden ver sin publicar, abriendo `docs/index.html` en el
navegador.)

## Nota sobre GitHub Pages

GitHub Pages solo puede servir contenido estático (HTML, CSS, JS): no puede
ejecutar un servidor Flask en Python. Por eso, en `docs/index.html` se
publicó una página con toda la documentación del proyecto (qué hace, cómo
ejecutarlo, las pruebas realizadas y las respuestas conceptuales) en lugar
de la API en funcionamiento. Para probar la API hay que clonar el
repositorio y ejecutarla localmente, como se explica arriba.
