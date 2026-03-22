
from modules.api_conect import sync_api, use_mode, save_api, load_api, start_api, export_api
from modules.utils_jshing import cursor, print_ident
from modules.menu import more

from modules.admin import control_user, get_users, get_info, relations
import modules.config as cfg

# Muestra el menu principal
more()

while True:

    try:

        commands_ = input(cursor())
        
        if commands_ == "exit":
            print("Finalizando programa ...")

            break

        allowed_command = globals().get(commands_)
        if not allowed_command:
            print("Comando ejecutado no existe, escirbe 'more' para ayuda.")
            continue

        
        cfg.config_jshing["in_function"] = commands_
        allowed_command()
        cfg.config_jshing["in_function"] = None

    except KeyboardInterrupt:
        print("\nFinalizando programa ...")
        break

    except Exception as err:
        print(f"ERROR: {err}")