from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
from fastapi.staticfiles import StaticFiles
import os
import glob

app = FastAPI()

# Configuración de conexión 
DB_CONFIG = {
    "host": "db",
    "user": "user",
    "password": "password",
    "database": "superhero",
    "port": 3306
}

def execute_query(query: str):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        return {"error": str(e)}
    finally:
        if connection.is_connected():
            connection.close()

def format_response(data, title: str, description: str = None):
    """Formatea la respuesta JSON con estructura organizada"""
    response = {
        "metadata": {
            "title": title,
            "description": description if description else title,
            "count": len(data) if isinstance(data, list) else 1
        },
        "data": data.to_dict(orient='records') if isinstance(data, pd.DataFrame) else data
    }
    return JSONResponse(
        content=response,
        media_type="application/json",
        status_code=200
    )

# Consulta 1: Top 10 superhéroes más altos con sus poderes
@app.get("/top-altos", response_class=JSONResponse)
async def get_top_altos():
    query = """
    SELECT 
        superhero.superhero_name as nombre,
        superpower.power_name as poder,
        superhero.height_cm as altura_cm
    FROM superhero
    JOIN hero_power ON superhero.id = hero_power.hero_id
    JOIN superpower ON hero_power.power_id = superpower.id
    ORDER BY superhero.height_cm DESC
    LIMIT 10;
    """
    df = execute_query(query)
    return format_response(
        df,
        "Top 10 Superhéroes más altos",
        "Lista de los superhéroes más altos con sus respectivos poderes"
    )

# Consulta 2: Editorial con más superhéroes y sus poderes
@app.get("/editorial-mas-heroes", response_class=JSONResponse)
async def get_editorial_mas_heroes():
    query = """
    SELECT 
        publisher.publisher_name as editorial,
        COUNT(superhero.id) AS total_heroes,
        GROUP_CONCAT(DISTINCT superpower.power_name) AS poderes
    FROM superhero
    JOIN publisher ON superhero.publisher_id = publisher.id
    JOIN hero_power ON superhero.id = hero_power.hero_id
    JOIN superpower ON hero_power.power_id = superpower.id
    GROUP BY publisher.publisher_name
    ORDER BY total_heroes DESC;
    """
    df = execute_query(query)
    return format_response(
        df,
        "Editoriales con más superhéroes",
        "Ranking de editoriales por cantidad de superhéroes y sus poderes"
    )

# Consulta 3: Superhéroes con más poderes
@app.get("/heroes-mas-poderes", response_class=JSONResponse)
async def get_heroes_mas_poderes():
    query = """
    SELECT 
        superhero.superhero_name as nombre,
        publisher.publisher_name as editorial,
        COUNT(hero_power.power_id) AS total_poderes
    FROM superhero
    JOIN hero_power ON superhero.id = hero_power.hero_id
    JOIN publisher ON superhero.publisher_id = publisher.id
    GROUP BY superhero.superhero_name, publisher.publisher_name
    ORDER BY total_poderes DESC
    LIMIT 10;
    """
    df = execute_query(query)
    return format_response(
        df,
        "Superhéroes con más poderes",
        "Top 10 de superhéroes con mayor cantidad de poderes"
    )

# Página de inicio con los endpoints disponibles
@app.get("/")
async def home():
    return {
        "api": "Superhéroes API",
        "version": "1.0",
        "endpoints": [
            {
                "path": "/top-altos",
                "description": "Top 10 superhéroes más altos con sus poderes",
                "example": "http://localhost:8010/top-altos"
            },
            {
                "path": "/editorial-mas-heroes",
                "description": "Editorial con más superhéroes y sus poderes",
                "example": "http://localhost:8010/editorial-mas-heroes"
            },
            {
                "path": "/heroes-mas-poderes",
                "description": "Superhéroes con más poderes",
                "example": "http://localhost:8010/heroes-mas-poderes"
            }
        ]
    }

#Consultas SQL para tablas, creadas en HTML

#Tabla con top 20 SuperHeroes: http://localhost:8010/tabla-superheroes

@app.get("/tabla-superheroes", response_class=HTMLResponse)
async def mostrar_tabla():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        query = """
        SELECT 
            sh.superhero_name AS Nombre,
            a.alignment AS Alineación,
            p.publisher_name AS Editorial,
            r.race AS Raza,
            g.gender AS Género
        FROM superhero sh
        LEFT JOIN alignment a ON sh.alignment_id = a.id
        LEFT JOIN publisher p ON sh.publisher_id = p.id
        LEFT JOIN race r ON sh.race_id = r.id
        LEFT JOIN gender g ON sh.gender_id = g.id
        LIMIT 20
        """
        df = pd.read_sql(query, connection)
        
        # Tabla con estilos Bootstrap
        html = df.to_html(
            classes="table table-striped table-bordered",
            index=False,
            justify="center"
        )
        
        return f"""
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <title>Superhéroes</title>
            </head>
            <body class="container mt-4">
                <h1 class="text-center mb-4">Top 20 Superhéroes</h1>
                {html}
            </body>
        </html>
        """

    except Error as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"
    finally:
        if connection.is_connected():
            connection.close()
            
#Tabla con top 15 herores por cantidad de Poderes: http://localhost:8010/tabla-poderes            
            
@app.get("/tabla-poderes", response_class=HTMLResponse)
async def mostrar_poderes():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        query = """
        SELECT 
            sh.superhero_name AS Héroe,
            GROUP_CONCAT(DISTINCT p.power_name SEPARATOR ', ') AS Poderes,
            COUNT(DISTINCT hp.power_id) AS Cantidad_Poderes,
            a.alignment AS Alineación
        FROM superhero sh
        LEFT JOIN hero_power hp ON sh.id = hp.hero_id
        LEFT JOIN superpower p ON hp.power_id = p.id
        LEFT JOIN alignment a ON sh.alignment_id = a.id
        GROUP BY sh.id, a.alignment
        ORDER BY Cantidad_Poderes DESC
        LIMIT 15
        """
        df = pd.read_sql(query, connection)
        
        html = df.to_html(
            classes="table table-hover table-dark", 
            index=False,
            justify="center",
            border=0,
            na_rep="Sin poderes"
        )
        
        return f"""
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <title>Poderes de Superhéroes</title>
                <style>
                    body {{
                        background-color: #f8f9fa;
                    }}
                    .table-dark {{
                        background-color: #343a40;
                    }}
                    h1 {{
                        color: #dc3545;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                    }}
                </style>
            </head>
            <body class="container mt-4">
                <h1 class="text-center mb-4">Top 15 Héroes por Cantidad de Poderes</h1>
                {html}
                <div class="mt-3 text-center">
                    <small class="text-muted">* Datos de la base de datos superhero</small>
                </div>
            </body>
        </html>
        """

    except Error as e:
        return f"""
        <html>
            <body class="container">
                <div class="alert alert-danger mt-4">
                    <h2>Error</h2>
                    <p>{str(e)}</p>
                </div>
            </body>
        </html>
        """
    finally:
        if connection.is_connected():
            connection.close()
            
#Super Heroes y sus detalles fisicos: http://localhost:8010/tabla-detalles
            
@app.get("/tabla-detalles", response_class=HTMLResponse)
async def mostrar_detalles():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        query = """
        SELECT 
            sh.superhero_name AS Héroe,
            CONCAT(sh.height_cm, ' cm') AS Altura,
            CONCAT(sh.weight_kg, ' kg') AS Peso,
            ec.colour AS Color_Ojos,
            hc.colour AS Color_Pelo,
            sc.colour AS Color_Piel,
            p.publisher_name AS Editorial
        FROM superhero sh
        LEFT JOIN colour ec ON sh.eye_colour_id = ec.id
        LEFT JOIN colour hc ON sh.hair_colour_id = hc.id
        LEFT JOIN colour sc ON sh.skin_colour_id = sc.id
        LEFT JOIN publisher p ON sh.publisher_id = p.id
        WHERE sh.height_cm IS NOT NULL
        ORDER BY sh.height_cm DESC
        LIMIT 15
        """
        df = pd.read_sql(query, connection)
        
        # Estilo tipo "cómic" con colores vibrantes
        html = df.to_html(
            classes="table table-bordered table-striped",
            index=False,
            justify="center",
            escape=False,
            formatters={
                'Color_Ojos': lambda x: f'<span style="background-color: {x}; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></span> {x}',
                'Color_Pelo': lambda x: f'<span style="background-color: {x}; width: 20px; height: 20px; display: inline-block;"></span> {x}',
                'Color_Piel': lambda x: f'<span style="background-color: {x}; width: 20px; height: 20px; display: inline-block;"></span> {x}'
            }
        )
        
        return f"""
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <title>Detalles Físicos</title>
                <style>
                    body {{
                        background-color: #f0f8ff;
                        font-family: 'Comic Sans MS', cursive;
                    }}
                    h1 {{
                        color: #ff6b6b;
                        text-align: center;
                        margin: 20px 0;
                        text-transform: uppercase;
                        letter-spacing: 3px;
                    }}
                    .table {{
                        box-shadow: 0 0 20px rgba(0,0,0,0.15);
                    }}
                    th {{
                        background-color: ##f8f9fa;
                        color: black !important;
                        border-bottom: 3px solid #4b0082;
                    }}
                    tr:hover {{
                        background-color: #fffacd !important;
                    }}
                </style>
            </head>
            <body>
                <div class="container-fluid mt-4">
                    <h1>⚡ Superhéroes: Detalles Físicos ⚡</h1>
                    <div class="table-responsive">
                        {html}
                    </div>
                    <div class="text-center mt-3">
                        <img src="https://i.imgur.com/JKt7v0l.png" width="100" alt="Logo cómic">
                    </div>
                </div>
            </body>
        </html>
        """

    except Error as e:
        return f"""
        <html>
            <body style="background-color: #ffe6e6">
                <div class="container mt-4 p-4 border border-danger rounded">
                    <h2 class="text-danger">¡Error!</h2>
                    <p>{str(e)}</p>
                    <button onclick="history.back()" class="btn btn-outline-danger">Volver</button>
                </div>
            </body>
        </html>
        """
    finally:
        if connection.is_connected():
            connection.close()
            
#Endpoint para mostrar todos los graficos hechos.            
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/graficos")
def listar_graficos():
    ruta_graficos = "static/graphs"
    archivos = glob.glob(f"{ruta_graficos}/*.png")
    
    urls = [
        {"nombre": os.path.basename(archivo), "url": f"http://localhost:8010/static/graphs/{os.path.basename(archivo)}"}
        for archivo in archivos
    ]
    
    return JSONResponse(content={"graficos_disponibles": urls})