# 🦸‍♂️ Superheroes API

Este proyecto es una API desarrollada con **FastAPI**, Docker y phpMyAdmin, que permite consultar y visualizar una base de datos de superhéroes. También incluye gráficas generadas con Pandas y Seaborn, asi como también incluye tablas en formato HTML.

## 📁 Estructura del Proyecto

SQL-PHP-FST/
├── app/
│ ├── main.py
│ ├── requirements.txt
│ ├── Dockerfile
│ └── static/
│ └── graphs/
│ ├── top_publishers.png
│ ├── alignment_distribution.png
│ └── gender_distribution.png
├── database_game/
│ ├── 01_reference_data.sql
│ ├── 02_hero_attribute.sql
│ └── 03_hero_power.sql
├── .env
├── docker-compose.yml
└── README.md


## 🚀 ¿Cómo ejecutar este proyecto?

### Requisitos

- Docker
- Docker Compose
- VSCode o editor similar

### Pasos para ejecutar

1. Clona este repositorio:

```bash
git clone https://github.com/Nefta2806/Superheroes-API.git
cd Superheroes-API
```

2. Inicia los contenedores:

```bash 
docker compose up
```

## ✅ La base de datos

Se utilizaron archivos .sql para crear y poblar la base de datos Super_heores. Estos archivos se encuentran en la carpeta database_game/:

    - 01_reference_data.sql

    - 02_hero_attribute.sql

    - 03_hero_power.sql

La base de datos fue importada a través de phpMyAdmin, accesible desde:

➡️ http://localhost:8080

## ✅ Consultas básicas.

Con un total de 6 consultas, 3 son posibles de ver a través del siguiente link para visualizar en FastAPI:
    ➡️ http://localhost:8010/
    
O acceder a cada consulta con los siguientes links: 
    - Superhéroes con más poderes
    ➡️ http://localhost:8010/heroes-mas-poderes

    - Editorial con más superhéroes
    ➡️ http://localhost:8010/editorial-mas-heroes

    - Top 10 superhéroes más altos
    ➡️ http://localhost:8010/top-altos

Las otras 3 consultas son posibles de ver con el archivo ConsultasPHP.sql, importando el archivo 
en el siguiente link:

➡️ http://localhost:8080

Al entrar, buscar la pestaña que diga "Importar" y subir el archivo con formato "SQL" y subir el archivo ya dicho "ConsultasPHP.sql"

## ✅ Crear la API REST con FastAPI

Se desarrolló una API con FastAPI para consultar los datos de las tablas de la base. Los archivos principales están en la carpeta app/:

    - main.py: contiene la lógica de conexión y los endpoints

    - requirements.txt: librerías necesarias

    - Dockerfile: definición de la imagen para FastAPI

La API se ejecuta con Docker Compose desde el archivo docker-compose.yml ubicado en la raíz (SQL-PHP-FST/).

La documentación de la API está disponible en:

➡️ http://localhost:8010/docs

## 📋 Generación de Tablas Dinámicas
Las tablas HTML de este proyecto fueron creadas mediante un proceso automatizado que combina:

    Pandas: Para transformar datos SQL en estructuras tabulares

    FastAPI: Como servidor web que entrega el HTML

    Bootstrap 5: Para estilos profesionales listos para producción

🔄 Flujo de Trabajo
Extracción de datos:

    Consultas SQL a la base de datos MySQL

    Resultados convertidos a DataFrames de Pandas

    Conversión a HTML (python):
### Transformación a tabla HTML con clases de Bootstrap

```python
html = df.to_html(
    classes="table table-striped table-bordered",
    index=False,
    justify="center",
    border=1
)
```
✨ Características Clave
    -Actualización automática: Los datos siempre reflejan el estado actual de la BD
    -Diseño profesional: Estilo limpio con:
    -Filas alternas coloreadas (table-striped)
    -Bordes visibles (table-bordered)
    -Texto centrado
    -Optimizado para móviles: Adaptable a diferentes tamaños de pantalla

### 🔧 Links para acceder a las tablas:

-Tabla con top 20 SuperHeroes: http://localhost:8010/tabla-superheroes
-Tabla con top 15 herores por cantidad de Poderes: http://localhost:8010/tabla-poderes
-Super Heroes y sus detalles fisicos: http://localhost:8010/tabla-detalles

## ✅ Generación de gráficas con Pandas y Seaborn

Se generaron gráficas a partir de los datos de la base de datos, las cuales fueron guardadas en la carpeta:
app/static/graphs/

Y se pueden consultar a partir del siguiente menú:
➡️ http://localhost:8010/graficos

Tambien se pueden consultar los gráficos con links directos:

1. Top 10 publishers con más superhéroes
➡️ http://localhost:8010/static/graphs/top_publishers.png
![Gráfico de compañías editoriales con más superhéroes](http://localhost:8010/static/graphs/top_publishers.png)

2. Distribución de alineamiento
➡️ http://localhost:8010/static/graphs/gender_distribution.png
![Gráfico de distribución por género de los superhéroes](http://localhost:8010/static/graphs/gender_distribution.png)

3. Distribución de género (Gráfico circular)
➡️ http://localhost:8010/static/graphs/alignment_distribution.png
![Gráfico de distribución de alineaciones](http://localhost:8010/static/graphs/alignment_distribution.png)

## 📊 Tecnologías Usadas
    - Python 3.11
    - FastAPI
    - Pandas / Seaborn
    - Docker
    - phpMyAdmin
    - MySQL

## ✏️ Autor

Neftalí - Nefta2806 en GitHub

