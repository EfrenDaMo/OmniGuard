# 🛡️🌐 OmniGuard - Sistema de Control de Acceso "Seguro"

Una plataforma web basada en flask para autenticacion segura, manejo de usuarios y control de sesión.


## Tabla de contenidos
- [Características Clave](<README#🚀 Características Clave:>)
- [Tecnologías Utilizadas](<README#💻 Tecnologías Utilizadas>)
- [Instalación](<README#📥 Instalación>)
- [Configuración](<README#⚙️  Configuración>)
- [Documentación API](<README#📚 Documentación API>)
- [Licencia](<README#📜 Licencia>)

### 🚀 Características Clave:
- **Encriptación de Nivel Militar**: Cifrado simétrico con Fernet para almacenamiento de contraseñas
- **Gestión de Sesiones**: Cookies seguras con políticas SameSite
- **Límite de Intentos**: 5 intentos de login/minuto contra ataques de fuerza bruta
- **Auditoría Detallada**: Sistema de logging estructurado en todos los módulos
- **Control de Acceso**: Decorador @require_login para rutas protegidas
- **Transacciones ACID**: Operaciones atómicas con MariaDB

### 💻 Tecnologías Utilizadas
![Python](https://img.shields.io/badge/Python-3.13.%2B-blue?logo=python&logoColor=yellow&logoSize=auto)
![Flask](https://img.shields.io/badge/Flask-3.1.x-lightgrey?logo=flask&logoSize=auto)
![MariaDB](https://img.shields.io/badge/MariaDB-11.7.2--1-orange?logo=mariadb&logoSize=auto)

| **Componente** | **Tecnología**                         |
|----------------|----------------------------------------|
| Framework Web  | Flask + Blueprints                     |
| Base de Datos  | MariaDB con transacciones ACID         |
| Seguridad      | Fernet (AES-128-CBC) + Cookies Seguras |
| Logging        | Sistema personalizado                  |

### 📥 Instalación

### ⚙️  Configuración

### 📚 Documentación API

### 📜 Licencia
Licencia MIT - Ver LICENSE.md para detalles
