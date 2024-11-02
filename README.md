# Automatización de SEO en WordPress con Selenium y OpenAI

### Descripción del proyecto
Este proyecto está diseñado para agilizar y automatizar la gestión de **SEO en mi blog de WordPress**, específicamente para añadir frases clave y meta descripciones en el plugin **Yoast SEO**. La idea es evitar el proceso manual de configurar el SEO de cada entrada, haciéndolo de forma más rápida y eficiente gracias a la ayuda de **Selenium** y **OpenAI**.

### ¿Cómo funciona?
Este script se conecta automáticamente al panel de administración de WordPress y navega hasta la sección de edición de cada entrada. Aquí aplica las frases clave y meta descripciones en los campos de Yoast SEO usando datos generados previamente. Todo el proceso es guiado por Selenium, que emula las interacciones en el navegador, mientras que **OpenAI** se encarga de generar las frases clave y descripciones para optimizar el SEO de cada publicación.

### Principales funcionalidades
1. **Generación automática de frases clave y meta descripciones**:  
   Mediante la API de OpenAI, se crean frases clave y meta descripciones basadas en el contenido de cada entrada del blog, maximizando la optimización SEO.

2. **Automatización de la inclusión de SEO en WordPress**:  
   Con Selenium, el script accede a la interfaz de administración de WordPress, abre cada entrada y coloca automáticamente la frase clave y la meta descripción en el plugin Yoast SEO.

3. **Actualización del estado en un archivo Excel**:  
   Las entradas procesadas se registran y marcan como actualizadas en un archivo Excel para llevar un seguimiento y evitar duplicaciones.

### Requisitos del proyecto
Para ejecutar este proyecto, necesitarás instalar los siguientes paquetes de Python:

```bash
pip install pandas selenium webdriver-manager requests openai langchain

También necesitas configurar un entorno virtual y generar un archivo `requirements.txt` para gestionar las dependencias del proyecto. Si deseas que Git ignore el entorno virtual, agrega la carpeta correspondiente (`env/` o `venv/`) a tu archivo `.gitignore`.

### Cómo usarlo
1. **Configura las credenciales**: Ingresa tu usuario y contraseña de WordPress y tu clave API de OpenAI en el archivo de configuración.
2. **Ejecuta el script**: Inicia el script y déjalo trabajar. Este abrirá el navegador, iniciará sesión en tu WordPress y comenzará a procesar las entradas automáticamente.
3. **Revisa el archivo Excel**: Al final del proceso, el archivo Excel se actualizará con el estado de cada entrada, indicando cuáles ya tienen frases clave y meta descripciones.

### Tecnologías utilizadas
- **Selenium**: Para la automatización de acciones en el navegador.
- **OpenAI**: Para generar frases clave y meta descripciones de manera inteligente y optimizada.
- **pandas**: Para la manipulación del archivo Excel que lleva el control de las entradas procesadas.
- **webdriver-manager**: Para gestionar el controlador de Chrome sin necesidad de descargas manuales.

### Notas adicionales
- **Seguridad**: Recuerda no compartir tu archivo `requirements.txt` ni las credenciales de WordPress o OpenAI en GitHub. La clave de API y las credenciales se reemplazan en el código con "xxxxx" para mantener la seguridad.
- **Compatibilidad**: Asegúrate de usar la versión más actualizada de Chrome y de `chromedriver` para evitar problemas de compatibilidad.

### Próximos pasos
El objetivo a largo plazo es seguir optimizando el flujo de trabajo SEO en WordPress. Esto podría incluir mejoras en la generación de contenido y en el análisis de rendimiento de las frases clave.
