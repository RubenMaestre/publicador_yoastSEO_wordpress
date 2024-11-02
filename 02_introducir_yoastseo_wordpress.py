import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException

# Configuración para WordPress
# Aquí pongo la URL de inicio de sesión y configuro las credenciales para entrar en el panel de administración de WordPress.
wordpress_url = "https://www.rubenmaestre.com/wp-login.php"
wp_username = "xxxxx"  # usuario de WordPress reemplazado
wp_password = "xxxxx"  # contraseña protegida

# Cargar el archivo Excel con los datos
# En este paso, especifico la ruta del archivo Excel que contiene las frases clave y meta descripciones.
excel_path = "frase_clave_meta_descripcion.xlsx"
df = pd.read_excel(excel_path)

# Verifico si ya existe una columna llamada "Actualizado". Si no está, la añado para marcar luego qué entradas he procesado.
if "Actualizado" not in df.columns:
    df["Actualizado"] = False

# Filtro las filas que no están marcadas como actualizadas, así solo proceso las entradas que realmente necesitan cambios.
df_pendientes = df[df["Actualizado"] == False]

# Inicializo el navegador usando Selenium. Aquí uso ChromeDriverManager para que busque automáticamente el controlador correcto.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Función para iniciar sesión en WordPress
# Con esta función abro la página de inicio de sesión, espero a que carguen los campos y los relleno con mis credenciales.
def login_wordpress():
    driver.get(wordpress_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(wp_username)
    driver.find_element(By.ID, "user_pass").send_keys(wp_password)
    driver.find_element(By.ID, "wp-submit").click()

# Función para actualizar la frase clave y la meta descripción de Yoast SEO en una entrada específica
# Aquí paso el `post_id`, `frase_clave` y `meta_descripcion` para la entrada que voy a actualizar.
def actualizar_entrada(post_id, frase_clave, meta_descripcion):
    # Accedo a la página de edición de la entrada usando el ID del post.
    driver.get(f"https://www.rubenmaestre.com/wp-admin/post.php?post={post_id}&action=edit")
    
    # Espero a que cargue el campo de frase clave de Yoast SEO, lo limpio y añado la nueva frase clave.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "focus-keyword-input-metabox"))).clear()
    driver.find_element(By.ID, "focus-keyword-input-metabox").send_keys(frase_clave)
    
    # Luego busco el campo de meta descripción y hago lo mismo: lo activo, lo limpio y añado la nueva descripción.
    meta_description_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "yoast-google-preview-description-metabox"))
    )
    meta_description_box.click()  # Hago clic para asegurarme de que el cuadro está activo
    meta_description_box.clear()
    meta_description_box.send_keys(meta_descripcion)

    # Intento hacer clic en el botón "Publicar" o "Actualizar" usando JavaScript por si hay interferencias visuales en la página.
    try:
        publicar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "publish"))
        )
        driver.execute_script("arguments[0].click();", publicar_btn)
        time.sleep(2)  # Espero un poco para asegurarme de que se guarden los cambios
        print(f"Entrada con ID {post_id} actualizada con éxito.")
        return True  # Devuelvo True si todo va bien
    except ElementClickInterceptedException:
        print(f"Error al hacer clic en el botón de publicación para la entrada con ID {post_id}")
        return False  # Devuelvo False si hubo un problema al hacer clic

# Iniciar sesión en WordPress antes de empezar las actualizaciones
login_wordpress()

# Recorro el DataFrame y actualizo cada entrada que tenga pendiente
for index, row in df_pendientes.iterrows():
    post_id = row['ID']
    frase_clave = row['Frase Clave']
    meta_descripcion = row['Meta Descripción']
    
    if actualizar_entrada(post_id, frase_clave, meta_descripcion):
        # Si la actualización fue bien, marco la entrada como "actualizada" en el DataFrame original.
        df.loc[df['ID'] == post_id, 'Actualizado'] = True
    else:
        print(f"Error al procesar la entrada con ID {post_id}")

# Una vez terminado, guardo los cambios en el archivo Excel original para mantener registro de las entradas ya procesadas.
df.to_excel(excel_path, index=False)
print("Archivo Excel actualizado con la columna 'Actualizado'.")

# Cierro el navegador al finalizar para liberar recursos
driver.quit()
