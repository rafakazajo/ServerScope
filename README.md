# ServerScope

Sistema de monitoreo de infraestructura híbrida diseñado para supervisar servidores Linux (Ubuntu) y Windows de manera centralizada.

## Arquitectura
Este proyecto implementa una solución de telemetría ligera y automatizada:
- **Nodo Central:** Base de datos MySQL alojada en AWS (RDS/EC2).
- **Agente Linux:** Script en Python desplegado vía Docker con persistencia de logs.
- **Agente Windows:** Script en Python (`.pyw`) ejecutado como proceso del sistema (`SYSTEM`) mediante el Programador de Tareas, utilizando Nmap para descubrimiento de puertos.

## Tecnologías utilizadas
- **Lenguaje:** Python 3.x
- **Contenedores:** Docker & Docker Compose (para el nodo Linux).
- **Bases de Datos:** MySQL/MariaDB.
- **Seguridad:** Automatización mediante Git para control de versiones y exclusión de credenciales (.gitignore).

## Configuración
1. **Clonar el repositorio:** `git clone https://github.com/rafakazajo/ServerScope.git`
2. **Dependencias:** Instalar librerías requeridas mediante `pip install -r requirements.txt`.
3. **Despliegue:**
   - En Linux: Usar `docker-compose up -d`.
   - En Windows: Configurar el `.pyw` en el Programador de Tareas con privilegios elevados.

## Notas de seguridad
El proyecto utiliza un `.gitignore` estricto para evitar la exposición de archivos de configuración (`config.py`), logs y datos sensibles del sistema.
