# UCA Planner

Este es el repositorio del UCA Planner, el organizador de horarios favorito de la UCA, desarrollado por alumnos de la institución.

# Funcionalidad

UCA Planner es el encargado de poder organizar los horarios dentro de un cronograma de horarios y al mismo
tiempo poder realizar la inscripción a las materias elegidas de cada comisión.

# Cómo correr el proyecto localmente

Requisitos: **Python 3** y **Docker Desktop** (reemplaza a XAMPP; no hace falta instalar MySQL a mano).

### 1. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 2. Levantar la base de datos (MariaDB en Docker)

```bash
docker compose up -d
```

La primera vez descarga MariaDB, crea la base `ucaplanner_base` e importa
automáticamente `doc/ucaplanner_base.sql`. Los datos quedan guardados en un
volumen de Docker, así que persisten entre reinicios.

### 3. Ejecutar la aplicación

```bash
python run.py
```

Abrir en el navegador: **http://localhost:5000**

### Comandos útiles de la base de datos

```bash
docker compose stop     # detener la base
docker compose start    # volver a arrancarla
docker compose down     # eliminar el contenedor (los datos se conservan en el volumen)
docker compose down -v  # eliminar TODO, incluidos los datos (reimporta el dump al volver a subir)
```

La conexión (host `localhost`, user `root`, sin contraseña, base `ucaplanner_base`)
está configurada en `_mysql_db.py`.


