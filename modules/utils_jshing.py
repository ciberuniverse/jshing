import json
import modules.config as cfg

def honey_connected() -> bool:

    if not cfg.config_jshing["honey_url"]:
        print("No estas conectado a ninguna API-REST")
        return False
    
    return True

def cursor() -> str:

    init_ = "jshing::"

    if cfg.config_jshing["local_mode"]:
        init_ += "[ LOCAL ]::"
    else:
        init_ += "[ API-REST ]::"
    
    if not cfg.config_jshing["in_function"]:
        return init_ + " >> "

    init_ += cfg.config_jshing["in_function"] + " >> "

    return init_

def print_ident(response_bdd: dict) -> None:
    print(json.dumps(response_bdd, indent=5))