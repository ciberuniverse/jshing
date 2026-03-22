def more():
    print("""
JSHING V1.1.0 => Defend to Attack
          
----------- Sincronizacion
          
>> use_mode     Encargado de establecer uso desde la API-REST de JSHING o modificando la base de datos local.
>> sync_api     Establece conexion al servidor o IP que hostea la API-REST de JSHING.
>> save_api     Guarda la conexion para un acceso rapido.
>> load_api     Carga y establece la conexion con la API-REST de JSHING.

>> start_api    Inicia el servidor con la api integrada para su uso.
>> export_api   Exporta el servidor para ser utilizado en la nube.

----------- Gestion de Usuarios
          
>> control_user Controla el navegador de un atacante con payloads javascripts y html, modificando su comportamiento.
>> get_users    Obtienes los navegadores maliciosos identificados por JSHING.
>> get_info     Obten la informacion de un atacante mediante fingerprint desde el frontend.
>> relations    Relacionar huellas digitales dejadas en el servidor, con otras en base a un uuid_m.

----------- Ayuda General
          
>> more         Comandos disponibles
""")
        