# 🛡️🌐 OmniGuard - Sistema de Control de Acceso "Seguro"

Una plataforma web basada en flask para autenticacion segura, manejo de usuarios y control de sesión.

## Tabla de contenidos
- [Características Clave](#caracteristicas-clave)
- [Tecnologías Utilizadas](#tecnologias-utilizadas)
- [Instalación](#instalacion)
- [Configuración](#configuracion)
- [Documentación API](#documentacion-api)
- [Licencia](#licencia)

### <a id="caracteristicas-clave"></a>🚀 Características Clave:
- **Encriptación de Nivel Militar**: Cifrado simétrico con Fernet para almacenamiento de contraseñas
- **Gestión de Sesiones**: Cookies seguras con políticas SameSite
- **Límite de Intentos**: 5 intentos de login/minuto contra ataques de fuerza bruta
- **Auditoría Detallada**: Sistema de logging estructurado en todos los módulos
- **Control de Acceso**: Decorador @require_login para rutas protegidas
- **Transacciones ACID**: Operaciones atómicas con MariaDB

### <a id="tecnologias-utilizadas"></a>💻 Tecnologías Utilizadas
![Python](https://img.shields.io/badge/Python-3.13.%2B-blue?logo=python&logoColor=yellow&logoSize=auto)
![Flask](https://img.shields.io/badge/Flask-3.1.x-lightgrey?logo=flask&logoSize=auto)
![MariaDB](https://img.shields.io/badge/MariaDB-11.7.2--1-orange?logo=mariadb&logoSize=auto)

| **Componente** | **Tecnología**                         |
|----------------|----------------------------------------|
| Framework Web  | Flask + Blueprints                     |
| Base de Datos  | MariaDB con transacciones ACID         |
| Seguridad      | Fernet (AES-128-CBC) + Cookies Seguras |
| Logging        | Sistema personalizado                  |

### <a id="instalacion"></a>📥 Instalación

1. Clonar e Instalar dependencias

```bash
$ git clone https://github.com/EfrenDaMo/OmniGuard
$ cd OmniGuard
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

2. Configurar la Base de datos

```sql
CREATE DATABASE omniguard;

CREATE TABLE `usuario` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE USER 'omniuser'@'localhost' IDENTIFIED BY 'contraseña_segura';

GRANT ALL PRIVILEGES ON omniguard.* TO 'omniuser'@'localhost';
```

### <a id="configuracion"></a>⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto que contenga las siguientes variables.
Donde `+-+-+-+` representa el valor dado a la variable.

```ini
DB_USER=-+-+-+-+-+
DB_PORT=-+-+-+-+-+
DB_HOST=-+-+-+-+-+
DB_NAME=-+-+-+-+-+
DB_PASSWORD=-+-+-+
APP_KEY=-+-+-+-+-+
APP_HOST=-+-+-+-+-
APP_PORT=-+-+-+-+-
APP_DEBUG=-+-+-+-+
APP_SECRET=-+-+-+-
LOG_FILE=-+-+-+-+-
LOG_LEVEL=-+-+-+-+
```

Para `APP_KEY` hay que hacer lo siguiente:

1. Ejecutar python ya sea instalado o via un entorno virtual:
```bash
$ python
```

2. Ejecutar lo siguiente dentro de la consola de python y pegarlo dentro del `.env`:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### <a id="documentacion-api"></a>📚 Documentación API

#### 🔐 Endpoints de Autenticación

| **Endpoint**    | **Método** | **Descripción**                | **Autenticación Requerida** |
|-----------------|:----------:|--------------------------------|-----------------------------|
| `/api/registro` | POST       | Registrar nuevo usuario        | No                          |
| `/api/login`    | POST       | Iniciar sesión                 | No                          |
| `/api/logout`   | POST       | Cerrar sesión                  | Si                          |
| `/api/session`  | POST       | Verificar si hay sesión activa | No                          |


#### 🔐 Endpoints de Control de Usuario

| **Endpoint**                                   | **Método** | **Descripción**                                  | **Autenticación Requerida** |
|------------------------------------------------|:----------:|--------------------------------------------------|-----------------------------|
| `/api/users`                                   | GET        | Obtiene lista de usuarios                        | Si                          |
| `/api/users/update`                            | PUT        | Actualizar datos de un usuario                   | Si                          |
| `/api/users/delete/<int:id_usuario>`           | DELETE     | Eliminar un usuario                              | Si                          |
| `/api/users/decrypt-password/<int:id_usuario>` | GET        | Desencriptar contraseña de un usuario especifico | Si                          |

### <a id="licencia"></a>📜 Licencia
Licencia GPL-3.0 - Ver LICENSE para detalles
