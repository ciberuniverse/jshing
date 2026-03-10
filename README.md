# JSHING V1.1.0 - Defend to Attack

###### Autor: Hernan Miranda
###### LinkedIn: linkedin.com/in/hernan-mirand4/

**PROYECTO EN DESARROLLO** - Esta herramienta se encuentra actualmente en fase de desarrollo activo.

JSHING es una plataforma de seguridad ofensiva que opera bajo el principio "Defend to Attack" (Defender para Atacar). Detecta cuando los visitantes abren las herramientas de desarrollador del navegador y establece un canal de comando y control para tomar control del navegador del atacante.

![Imagen](https://repository-images.githubusercontent.com/1178138833/f7e8909b-f5b4-475b-858e-455059cc14ca)

## Tecnologías Utilizadas

### Backend
- **Python 3.7+**: Lenguaje principal del servidor
- **Flask**: Framework web para API REST
- **Mongita**: Base de datos NoSQL embebida

### Frontend
- **JavaScript ES6+**: Motor de detección y ejecución
- **HTML5**: Estructura de payloads
- **CSS3**: Estilos de interfaz

### Infraestructura
- **API REST**: Comunicación cliente-servidor
- **Sesiones Flask**: Gestión de identidad
- **Tokens SHA256**: Autenticación administrativa

## Enfoque y Propósito

JSHING está enfocado en **seguridad ofensiva y pruebas de penetración autorizadas**. Su propósito principal es:

- **Detección proactiva**: Identificar cuando usuarios maliciosos abren herramientas de desarrollador para inspeccionar o atacar el sitio
- **Toma de control**: Establecer un canal de comando y control sobre navegadores de atacantes
- **Investigación**: Recopilar información detallada sobre atacantes mediante fingerprinting avanzado
- **Defensa activa**: Responder a intentos de ataque con contramedidas automatizadas

## Instalación

### Prerrequisitos
- Python 3.7 o superior
- Navegador web moderno con JavaScript habilitado

### Pasos
1. Clonar el repositorio
   ```bash
   git clone https://github.com/ciberuniverse/jshing.git
   cd jshing
   ```

2. Instalar dependencias
   ```bash
   pip install flask mongita requests
   ```

3. Iniciar la aplicación
   ```bash
   python jshing.py
   ```

## Cómo Usar JSHING

### 1. Iniciar el Servidor API

Ejecuta el comando `start_api` en la CLI:

```bash
python jshing.py
> start_api
:: IP-USE :: 127.0.0.1
:: API-PORT :: 9090
```

El sistema generará un token de autenticación automáticamente:
### 2. Integrar en Sitio Web

Añade el script JavaScript en las páginas que deseas proteger:

```html
<script src="http://127.0.0.1:9090/static/jshing.js"></script>
```

### 3. Monitorear Actividad

Usa los comandos de gestión de usuarios:
```bash
> get_users          # Listar usuarios detectados
> get_info           # Obtener información detallada
> control_user       # Controlar navegador de atacante
```

### 4. Controlar Navegadores

El comando `control_user` permite inyectar payloads personalizados:

```bash
> control_user
:: UUID_M :: [uuid_del_usuario]
:: CONTROL MODE :: all
:: HTML PAYLOAD :: <div>Alerta de seguridad</div>
:: JSCRIPT PAYLOAD :: alert('Acceso detectado');
```

## Flujo de Operación

1. **Detección**: El cliente monitorea cada 2 segundos si se abren las DevTools usando técnicas de timing con `debugger`

2. **Fingerprinting**: Si se detectan, recopila 18+ características del navegador para crear una huella digital única (`uuid_m`) 

3. **Registro**: El sistema almacena la información del usuario y asigna un identificador persistente

4. **Control**: Los administradores pueden inyectar payloads que se ejecutan dinámicamente en el navegador objetivo

## Comandos Disponibles

### Sincronización 
- `use_mode`: Cambiar entre modo local y API-REST
- `sync_api`: Conectar a servidor API remoto
- `save_api`: Guardar configuración de conexión
- `load_api`: Cargar configuración guardada
- `start_api`: Iniciar servidor API integrado

### Gestión de Usuarios 
- `control_user`: Controlar navegador de atacante con payloads
- `get_users`: Listar navegadores maliciosos identificados
- `get_info`: Obtener información detallada de un atacante
- `relations`: Relacionar huellas digitales (en desarrollo)

## Modos de Operación

### Modo Local
- Acceso directo a la base de datos Mongita
- Ideal para desarrollo y pruebas
- Sin requerimientos de red

### Modo API-REST
- Comunicación vía HTTP con servidor Flask
- Adecuado para producción y despliegues distribuidos
- Requiere autenticación por token para endpoints administrativos

## Advertencia de Seguridad

Esta herramienta está diseñada exclusivamente para:
- Pruebas de penetración autorizadas
- Investigación de seguridad
- Propósitos educativos
- Demostraciones controladas

El uso no autorizado de esta herramienta puede ser ilegal. Utilízala únicamente en sistemas que tengas permiso explícito para probar.

## Estado del Desarrollo

- [x] Detección de herramientas de desarrollador
- [x] Fingerprinting avanzado
- [x] Inyección de payloads
- [x] CLI de administración
- [x] Modo local y API-REST
- [ ] Interfaz web de administración
- [ ] Sistema de alertas en tiempo real
- [ ] Análisis de comportamiento