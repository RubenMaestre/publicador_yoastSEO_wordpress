import requests
from requests.auth import HTTPBasicAuth
import openai
from langchain.chat_models import ChatOpenAI
import pandas as pd
import os

# Aquí configuro la API de WordPress y OpenAI, las dos herramientas principales que voy a usar en este script.
# Primero, establezco la URL de los posts en mi WordPress.
wp_url_posts = 'https://www.rubenmaestre.com/wp-json/wp/v2/posts'
# Ahora configuro el usuario de WordPress. He cambiado la información sensible para proteger las credenciales.
wp_user = 'xxxxx'  # nombre de usuario del WordPress
wp_password = 'xxxxx'  # contraseña, también reemplazada
# Creo la autenticación HTTP básica, que necesito para acceder a la API de WordPress.
auth = HTTPBasicAuth(wp_user, wp_password)

# Configuración de OpenAI: sustituyo la clave de API por 'xxxxx' para mantener la seguridad.
openai.api_key = 'xxxxx'
# Aquí configuro el modelo de lenguaje que voy a usar, ajustando algunos parámetros para que genere textos bien optimizados.
# Yo tengo entrenado un modelo fine-tunning en OpenAI que es el que he utilizado.
llm = ChatOpenAI(
    model="xxxxx",  # modelo de OpenAI personalizado para mis necesidades
    temperature=0.7,  # este valor ajusta la creatividad de las respuestas
    max_tokens=1200,  # aquí limito la longitud de las respuestas generadas
    openai_api_key=openai.api_key
)

# Función para obtener una publicación de WordPress en bloques de una en una.
# Lo que hago aquí es acceder a los posts en formato JSON, lo cual me facilita extraer datos.
def obtener_publicacion(page, limit=1):
    # Realizo la petición a la API, paso el número de página y el límite de posts por página.
    response = requests.get(wp_url_posts, params={'per_page': limit, 'page': page}, auth=auth)
    if response.status_code == 200:
        # Si todo va bien, obtengo los datos en JSON y filtro solo los campos necesarios.
        posts = response.json()
        return [(post['id'], post['title']['rendered'], post['content']['rendered']) for post in posts]
    else:
        # En caso de error, lo reporto con el código de estado para saber qué pasó.
        print(f"Error al obtener publicaciones: {response.status_code}")
        return []

# Función para generar una frase clave SEO y una meta descripción optimizada.
# Aquí uso un modelo de lenguaje para crear estos elementos en base al título y contenido del blog.
def generar_frase_clave_y_meta_descripcion_finetuning(titulo, contenido):
    # Construyo el prompt que le paso al modelo de lenguaje. Aquí te pongo un ejemplo sencillo, se puede perfilar mucho más.
    prompt = (
        f"Basado en el siguiente título y contenido del blog, genera una frase clave SEO (máximo 6 palabras) "
        f"y una meta descripción optimizada (máximo 140 caracteres):\n\n"
        f"Título: {titulo}\n\nContenido:\n{contenido[:1000]}\n\n"
        f"Frase clave SEO:\nMeta descripción:"
    )
    
    try:
        # Envío el prompt al modelo y obtengo la respuesta
        response = llm.predict(prompt)
        resultado = response.strip().split("\n")
        
        # Extraigo la frase clave y la meta descripción de la respuesta
        frase_clave = ""
        meta_descripcion = ""
        for line in resultado:
            if "Frase clave SEO:" in line:
                frase_clave = line.replace("Frase clave SEO:", "").replace("*", "").strip()
            elif "Meta descripción:" in line:
                meta_descripcion = line.replace("Meta descripción:", "").replace("*", "").strip()
        
        # Verifico si el modelo generó los datos correctamente
        if not frase_clave:
            frase_clave = "Frase clave no generada"
        if not meta_descripcion:
            meta_descripcion = "Meta descripción no generada"
        
        return frase_clave, meta_descripcion
    except Exception as e:
        # En caso de error, devuelvo un mensaje de error para los datos
        print(f"Error al generar frase clave y meta descripción: {e}")
        return "Error en generación", "Error en generación"

# Cargar o crear el archivo Excel para guardar los resultados de frase clave y meta descripción.
excel_path = "frase_clave_meta_descripcion.xlsx"
if os.path.exists(excel_path):
    # Si el archivo ya existe, lo cargo y creo un conjunto con los IDs ya procesados.
    df_existente = pd.read_excel(excel_path)
    ids_existentes = set(df_existente['ID'])
else:
    # Si no existe, creo un DataFrame vacío con las columnas que necesito
    df_existente = pd.DataFrame(columns=["ID", "Título", "Frase Clave", "Meta Descripción"])
    ids_existentes = set()

# Lista para almacenar los resultados que voy generando
resultados = []
page = 1
continuar = True
contador = 0  # Contador para saber cuántas publicaciones he procesado (incluidas las omitidas)

# Bucle para obtener y procesar las publicaciones, una a una
while continuar:
    posts = obtener_publicacion(page, 1)
    
    for post_id, titulo, contenido in posts:
        # Verifico si ya he procesado este post para evitar duplicados.
        if post_id in ids_existentes:
            print(f"Entrada con ID {post_id} ya procesada, omitiendo...")
            contador += 1
            continue

        # Genero la frase clave y la meta descripción usando el modelo de lenguaje
        frase_clave, meta_descripcion = generar_frase_clave_y_meta_descripcion_finetuning(titulo, contenido)
        
        if frase_clave != "Error en generación" and meta_descripcion != "Error en generación":
            # Si la generación se hace bien, añado los resultados a la lista.
            resultados.append({"ID": post_id, "Título": titulo, "Frase Clave": frase_clave, "Meta Descripción": meta_descripcion})
            print(f"Entrada con ID {post_id} procesada con éxito.")
        else:
            print(f"Entrada con ID {post_id} error al procesar.")
        
        contador += 1
    
    # Cada 10 publicaciones pregunto si quiero continuar
    if contador % 10 == 0:
        respuesta = input("¿Quieres continuar con las siguientes 10 publicaciones? (Y/N): ").strip().upper()
        if respuesta == "N":
            continuar = False
        else:
            page += 1
    else:
        page += 1

# Combino los datos nuevos con los existentes y guardo en el archivo Excel.
df_nuevo = pd.DataFrame(resultados)
df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
df_final.to_excel(excel_path, index=False)
print("Archivo Excel generado/actualizado: frase_clave_meta_descripcion.xlsx")
