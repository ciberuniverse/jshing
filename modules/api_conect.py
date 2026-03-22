import requests, json, subprocess, time, shutil, os
import modules.config as cfg
from hashlib import sha256
from base64 import b64encode

from modules.utils_jshing import cursor, print_ident

# Guarda el archivo js para utilizar en un servidor externo
def __save_javascript_file__(url_api: str = None):
    """Funcion encargada de guardar jshing modificado con los datos recibidos"""

    # Si es que la funcion no se esta ocupando desde otra funcion (no recibe parametros) 
    if not url_api:
        url_api = cfg.config_jshing["honey_url"]
    
    try:
        with open("base_jshing.js", "r", encoding="UTF-8") as read_js, open("server/static/jshing.js", "w", encoding="UTF-8") as save_js:
            
            jshing_updated = read_js.read().replace("<< URL_ENDPOINT >>", url_api)
            save_js.write(jshing_updated)

        print(f'\n\nPara usar en tu pagina web: <script src="{url_api}/static/jshing.js"></script>')
        print(f"Para testear la funcion de la API desde tu navegador: {url_api}/admin")
        
    except:
        print("ERROR: No se logro modificar la ruta de la api en base_jshing.js")
        return

def __gen_token_api_key__() -> str:
    """Funcion encargada de enerar el token api para el funcionamiento del backend."""
    to_token = str(time.time()) + __file__
    return b64encode(sha256(to_token.encode("utf-8")).hexdigest().encode("utf-8")).decode("utf-8").replace("=", "")

def __validate_url__(url_honey: str) -> str | None:

    if any(x not in url_honey for x in ["http", "://"]):
        print("ERROR: El formato de tu URL debe de verse algo asi https://tudominio.com o tambien https://224.0.23.5:9092")
        return None
    
    url_honey = url_honey.strip()
    url_honey = url_honey[:-1] if url_honey.endswith("/") else url_honey

    return url_honey

def start_api():

    ip_use = input(cursor() + ":: IP-USE :: ")
    port_use = input(cursor() + ":: API-PORT :: ")

    signature = __gen_token_api_key__()

    # Se guarda el token de autorizacion y administracion en la sesion de config_jhshing
    cfg.config_jshing["token"] = signature

    # Ejecuta el inicio de la api desde un subproceso para utilizar jshing desde ahi
    exec_command =[
        "python",
        __file__.split("modules")[0].replace("\\", "/") + "server/api.py", # Ruta del archivo de la API en Flask
        ip_use, # Interfaz de ip sobre la que trabajara Flask
        port_use, # Puerto que usara Flask
        signature, # Firma que se debera de usar para utilizar los endpoints de admin
        "start_api" # Parametro para decirle a api.py que se esta usando desde fshing.py
    ]

    print(f"""
#############################################################################
#                          JSHING - PERSONALIZADO                           #
#############################################################################

╔═══════════════════════════════════════════════════════════════════════════╗
║  Para usar jshing de forma personalizada, sigue estas instrucciones:      ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────┐
│  >  Endpoints ADMIN (api/v2/admin/)                                       │
│     Debes incluir este HEADER en cada petición:                           │
│                                                                           │
│                        Token: {signature[:5]}...                                    │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│  >  Hosting en VPS o RENDER                                               │
│     Asigna una variable de entorno con el nombre:                         │
│                                                                           │
│                    SECRET_KEY_JSHING = {signature[:5]}...                           │
└───────────────────────────────────────────────────────────────────────────┘

TU TOKEN =>>
{signature}

Recuerda: La firma debe coincidir exactamente con la utilizada en el header.
    """)

    time.sleep(10)
    subprocess.run(exec_command) # Se inicia el subrpoceso

def use_mode():
    
    # Si el modo local modificando la base directamente se usa esa opcion, en caso contrario unicamente se usa la api
    if not cfg.config_jshing["local_mode"]:

        cfg.config_jshing["local_mode"] = True
        print("Modo local (modificando la base de datos directamente) activado.")
        return
    
    cfg.config_jshing["local_mode"] = False
    print("Modo API-REST activado.")
    return     

def save_api():

    cfg.config_jshing["in_function"] = None
    
    try:
        with open("config.jshing", "w", encoding="UTF-8") as save_r:
            save_r.write(json.dumps(cfg.config_jshing, indent=5))

    except:
        print("ERROR: No se logro guardar la conexion.")
        return
    
    print("Conexion guardada correctamente en: config.jshing")

def load_api():

    try:
        with open("config.jshing", "r", encoding="UTF-8") as read_c:
            cfg.config_jshing = json.loads(read_c.read())
    
    except:
        print("ERROR: No se logro cargar la conexion.")
        return
    
    # Se imprime el resultado de la carga de los datos y se modifica la ruta de conexion en JS
    print_ident(cfg.config_jshing)
    __save_javascript_file__()


def sync_api():

    while True:
        
        url_honey = input(cursor() + ":: URL-API :: ")
        token_api = input(cursor() + ":: TOKEN-API :: ")

        # Si la url no es valida se vuelve a iterar el input
        url_honey = __validate_url__(url_honey)
        if not url_honey:
            continue
        
        break
    
    try:
        result_endpoints = requests.get(url_honey + "/api/v2/admin", headers={"token": token_api})
        result_endpoints = result_endpoints.json()

    except:
        print(f"No fue posible conectarse a la url establecida {url_honey}.")
        return
    
    if "status" not in result_endpoints:
        print(f"La informacion retornada desde el endpoint {url_honey} no corresponde a una api de jshing")
        return
        
    ##### Se establece la configuracion global de los endpoints y se termina esta seccion
    cfg.config_jshing["endpoints_disponibles"] = result_endpoints
    cfg.config_jshing["honey_url"] = url_honey
    cfg.config_jshing["token"] = token_api

    print(f"Conectado a {cfg.config_jshing['honey_url']}")
    __save_javascript_file__()
    return

def export_api():

    print("[+] Ingresa el dominio raiz donde sera hosteado el servidor. EJ: https://hony.pythonanyware.com")
    while True:
        # Mientras la url no sea valida se volvera a solicitar el dominio
        url_honey = __validate_url__(input(cursor() + ":: DOMAIN :: "))

        # Si la url no es valida vuelve a pedir el dominio
        if not url_honey:
            continue

        break

    token_url = __gen_token_api_key__()

    # Se realiza un listado de las carpetas ubicadas en la ruta actual
    # si no se encuentra la carpeta server, se le solicita al usuario ejecutar jshing desde
    # la carpeta root de jshing
    carpetas_en_ruta = os.listdir(".")
    if "server" not in carpetas_en_ruta:
        print("[-] Ejecuta esto en la carpeta raiz de JSHING. La carpeta server no se encuentra en ruta.")
        return
    
    # Si existe ya una carpeta de servidor se borrara
    if "honey_host" in carpetas_en_ruta:
        shutil.rmtree("honey_host"); print("[+] Borrando archivos previos")

    # Se guarda el archvio que ejecutaran los clientes que abran y ejecuten el archivo js
    __save_javascript_file__(url_honey)

    # Se copian los archivos del server original a la ruta actual para su modificacion
    shutil.copytree("server", "honey_host"); print("[+] Archivos del servidor copiados a honey_host") 

    # Se establece la linea de remplazo, esta sera la encargada de administar el log dentro de admin
    replace = ':: HARDCODED_KEY ::'
    with open("honey_host/api.py", "r", encoding="UTF-8") as mod_api:    
        new_api_file = mod_api.read().replace(replace, token_url)

    # Se guarda la nueva version de el archivo api.py en la carpeta
    with open("honey_host/flask_app.py", "w", encoding="UTF-8") as mod_api_w:
        mod_api_w.write(new_api_file)
    
    # Se borra la version base creada
    os.remove("honey_host/api.py")

    print(f"""
=====================================================================
Pasos para usar JSHing como panel de administración en PythonAnywhere
=====================================================================

1. Sube la carpeta `honey_host` a tu servidor, dentro de la carpeta raíz web.
   (Ejemplo: `/home/tuusuario/honey_host`)

2. Asegúrate de usar la versión más reciente de Python (actualmente 3.12).
   Puedes verificarlo en la consola de PythonAnywhere.

3. Crea un entorno virtual para aislar las dependencias del proyecto:
   - Crea el entorno:   `mkvirtualenv api_jshing`
   - Actívalo:          `workon api_jshing`

4. Instala los paquetes requeridos desde el archivo `requirements.txt`:
   `python3.12 -m pip install -r requirements.txt`

5. Reinicia tu aplicación web desde el panel de control de PythonAnywhere
   (sección "Web") o mediante la consola con `touch /var/www/tuusuario_pythonanywhere_com_wsgi.py`.

TU TOKEN =>>
{token_url}
    """)
    return