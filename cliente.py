"""Cliente de consola: se conecta a la API para registrarse, iniciar sesión
y ver las tareas."""
import requests

BASE_URL = "http://localhost:5000"


def registrar():
    """Pide usuario y contraseña, y los envía a POST /registro."""
    usuario = input("Nuevo usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    try:
        respuesta = requests.post(
            f"{BASE_URL}/registro",
            json={"usuario": usuario, "contraseña": contrasena},
        )
        print(respuesta.json().get("message"))
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")


def iniciar_sesion():
    """Pide usuario y contraseña, y los envía a POST /login."""
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    try:
        respuesta = requests.post(
            f"{BASE_URL}/login",
            json={"usuario": usuario, "contraseña": contrasena},
        )
        datos = respuesta.json()
        print(datos.get("message"))
        return datos.get("status") == "success"
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")
        return False


def ver_tareas():
    """Consulta GET /tareas y muestra el HTML de bienvenida como texto plano."""
    try:
        respuesta = requests.get(f"{BASE_URL}/tareas")
        print("\n--- Respuesta del servidor (/tareas) ---")
        print(respuesta.text.strip())
        print("-----------------------------------------\n")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")


def menu():
    """Muestra el menú y despacha la opción elegida hasta que el usuario salga."""
    sesion_iniciada = False
    while True:
        print("\n1. Registrarse\n2. Iniciar sesión\n3. Ver tareas\n4. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            sesion_iniciada = iniciar_sesion()
        elif opcion == "3":
            if sesion_iniciada:
                ver_tareas()
            else:
                print("Primero tenés que iniciar sesión (opción 2).")
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
