# Pokédex App

Una aplicación de escritorio que permite a los usuarios gestionar sus equipos Pokémon, utilizando la PokeAPI para obtener información detallada de los Pokémon. Desarrollada con Python, CustomTkinter y MySQL.

## 🌟 Características

- 👤 Sistema de autenticación con roles (usuario/administrador)
- 🔍 Búsqueda y visualización de Pokémon
- 👥 Gestión de equipos personalizados
- 📊 Estadísticas detalladas
- 🎮 Personalización de Pokémon (apodos)
- 📱 Interfaz moderna y responsiva
- 📈 Panel de administración con análisis de datos

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- Pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/pokedex-app.git
cd pokedex-app
```

2. Crear un entorno virtual:
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
# Crear la base de datos en MySQL
mysql -u root -p
CREATE DATABASE pokedex_app;
USE pokedex_app;

# Ejecutar el script de la base de datos
mysql -u root -p pokedex_app < database/schema.sql
```

5. Configurar el archivo config.ini:
```ini
[DATABASE]
host = localhost
user = tu_usuario
password = tu_contraseña
database = pokedex_app
port = 3306
```

## 🚀 Uso

1. Iniciar la aplicación:
```bash
python main.py
```

2. Iniciar sesión o registrarse:
   - Crear una nueva cuenta desde la pantalla de inicio
   - Usar credenciales existentes

3. Funcionalidades principales:
   - Buscar Pokémon usando la barra de búsqueda
   - Añadir Pokémon a tu equipo
   - Ver estadísticas de tu equipo
   - Personalizar apodos de tus Pokémon
   - Gestionar tu perfil de entrenador

## 👥 Roles de Usuario

### Usuario Normal
- Buscar y ver información de Pokémon
- Crear y gestionar equipo personal
- Personalizar perfil de entrenador
- Ver estadísticas personales

### Administrador
- Todas las funciones de usuario normal
- Gestionar usuarios
- Ver estadísticas globales
- Monitorear actividad del sistema
- Gestionar roles de usuario

## 📁 Estructura del Proyecto

```
pokedex_app/
│
├── config/
│   ├── __init__.py
│   ├── database.py
│   ├── constants.py
│   └── config_handler.py
│
├── models/
│   ├── user_model.py
│   ├── pokemon_model.py
│   ├── trainer_model.py
│   ├── team_model.py
│   └── admin_model.py
│
├── views/
│   ├── login_view.py
│   ├── main_view.py
│   ├── search_view.py
│   ├── team_view.py
│   ├── profile_view.py
│   ├── admin_view.py
│   └── components/
│
├── controllers/
│   ├── auth_controller.py
│   ├── pokemon_controller.py
│   ├── team_controller.py
│   └── admin_controller.py
│
├── services/
│   ├── api_service.py
│   └── encryption_service.py
│
├── database/
│   └── schema.sql
│
├── assets/
│   └── images/
│
├── config.ini
├── requirements.txt
└── main.py
```

## 🔧 Configuración

La aplicación utiliza un archivo `config.ini` para gestionar las configuraciones:

- Conexión a base de datos
- Configuración de API
- Ajustes de seguridad
- Preferencias de aplicación
- Configuración de logging

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor abre un issue con:
- Descripción detallada del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Capturas de pantalla si es posible

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Para soporte y preguntas:
- Abrir un issue
- Enviar un email a: tu-email@ejemplo.com

## 🔄 Actualizaciones

La aplicación se actualiza regularmente. Para obtener la última versión:
```bash
git pull origin main
pip install -r requirements.txt
```

## ⚠️ Notas Importantes

- Hacer backup de la base de datos regularmente
- No compartir credenciales de administrador
- Mantener el archivo config.ini seguro
- Actualizar dependencias regularmente

## 🎉 Agradecimientos

- [PokeAPI](https://pokeapi.co/) por proporcionar los datos
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) por el framework GUI
- La comunidad de Python por las herramientas utilizadas