import requests, json, subprocess, time, os
import modules.config as cfg
from hashlib import sha256
from base64 import b64encode

from modules.utils_jshing import cursor, print_ident

# Guarda el archivo js para utilizar en un servidor externo
def __save_javascript_file__():
    
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

def start_api():

    ip_use = input(cursor() + ":: IP-USE :: ")
    port_use = input(cursor() + ":: API-PORT :: ")

    to_token = str(time.time()) + __file__
    signature = b64encode(sha256(to_token.encode("utf-8")).hexdigest().encode("utf-8")).decode("utf-8").replace("=", "")
    
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

        if any(x not in url_honey for x in ["http", "://"]):
            print("ERROR: El formato de tu URL debe de verse algo asi https://tudominio.com o tambien https://224.0.23.5:9092")
            continue
        
        url_honey = url_honey.strip()
        url_honey = url_honey[:-1] if url_honey.endswith("/") else url_honey
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