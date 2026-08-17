# Kurisu CLI Agent

Este repositorio contiene un agente de inteligencia artificial interactivo basado en línea de comandos, diseñado para interactuar con modelos de lenguaje avanzados de Google (Gemini). El agente está personalizado para ofrecer asistencia en tareas técnicas, gestión de archivos, ejecución de comandos del sistema, control de versiones Git, y ahora incluye funciones mejoradas para interacción web y gestión de medios, todo ello manteniendo un contexto conversacional persistente.

## Características Principales

*   **Interacción Conversacional:** Permite una comunicación fluida con el modelo de lenguaje, manteniendo el contexto de la conversación a través del historial.
*   **Ejecución de Comandos del Sistema:** Capacidad para ejecutar comandos de shell directamente en el sistema operativo, con mecanismos de seguridad para comandos que requieren privilegios elevados (`sudo`).
*   **Gestión y Edición de Archivos:** Herramientas para leer, escribir y realizar ediciones avanzadas en archivos (añadir contenido, insertar/borrar líneas, reemplazar texto).
*   **Control de Versiones Git:** Integración para realizar operaciones de `commit` en repositorios Git, facilitando la gestión del código fuente.
*   **Control de Música (Spotify):** Permite gestionar la reproducción de Spotify, incluyendo pausar, reanudar, saltar a la canción anterior/siguiente, y buscar/reproducir pistas específicas. Incluye una lógica para optimizar la búsqueda de canciones con nombres en japonés romanizado.
*   **Investigación y Extracción de Información Web:** Capacidad para realizar búsquedas en internet, extraer letras de canciones de sitios web y sintetizar información de páginas para responder a consultas complejas.
*   **Personalidad Definida:** Configurado con instrucciones de sistema para guiar el comportamiento y tono del agente.
*   **Gestión de Claves API:** Soporte para múltiples claves API de Gemini.
*   **Entorno Aislado:** Utiliza un entorno virtual de Python (`venv`) para gestionar las dependencias del proyecto de forma limpia y aislada.

## Tecnologías Utilizadas

*   **Python 3.x**
*   **Google Gemini API:** Para la interacción con modelos de lenguaje avanzados.
*   **`python-dotenv`:** Para la gestión segura de variables de entorno (claves API).
*   **`colorama`:** Para estilizar la salida de la terminal.
*   **`subprocess`:** Para la ejecución de comandos del sistema.
*   **`requests`:** Para realizar solicitudes HTTP y obtener contenido de páginas web.
*   **`BeautifulSoup4`:** Para el parseo y extracción de datos de documentos HTML.
*   **`spotipy`:** Biblioteca de cliente de Python para la API de Spotify Web, utilizada para el control de reproducción y búsqueda de canciones.
*   **`selenium` y `webdriver_manager`:** (Detectadas como dependencias, útiles para automatización web, aunque no se hayan implementado completamente para la interacción actual).

## Configuración y Ejecución

Sigue estos pasos para configurar y ejecutar el Kurisu CLI Agent en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [URL_DE_TU_REPOSITORIO] # Reemplaza con la URL real
    cd KURISU_CLI_AGENT
    ```

2.  **Configurar el Entorno Virtual:**
    Es fundamental crear y activar un entorno virtual para gestionar las dependencias.
    ```bash
    python3 -m venv bot-env
    source bot-env/bin/activate
    ```

3.  **Instalar Dependencias:**
    Instala todas las librerías necesarias utilizando el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del directorio del proyecto y añade tus claves API de Google Gemini y las credenciales de Spotify (si aplica para futuras integraciones más profundas).
    ```
    # .env
    GEMINI_KEYS="TU_CLAVE_API_1,TU_CLAVE_API_2" # Puedes añadir múltiples claves separadas por comas
    # SPOTIPY_CLIENT_ID="TU_CLIENT_ID_SPOTIFY"
    # SPOTIPY_CLIENT_SECRET="TU_CLIENT_SECRET_SPOTIFY"
    ```

5.  **Configurar Personalidad del Agente y Modelo:**
    Revisa los archivos en el directorio `configs/` (`Kurisu_config.json`, `system_instruction.md`) para ajustar los parámetros del modelo de lenguaje y la instrucción de sistema que define la personalidad y comportamiento del agente.

6.  **Ejecutar el Agente:**
    Con el entorno virtual activado, ejecuta el script principal:
    ```bash
    python3 main.py
    ```

7.  **Desactivar el Entorno Virtual (cuando termines):**
    ```bash
    deactivate
    ```

## Estructura del Proyecto

*   `main.py`: Punto de entrada principal y orquestador del agente.
*   `Functions.py`: Contiene las implementaciones de las herramientas que el agente puede invocar (ejecución de comandos, manipulación de archivos, Git commits).
*   `Web_functions.py`: Módulo que encapsula las funciones relacionadas con la interacción web (búsqueda en internet, parseo de HTML).
*   `Chats_history.py`: Módulo para la carga y guardado del historial de conversaciones.
*   `Utilities.py`: Funciones de utilidad generales y auxiliares.
*   `configs/`: Directorio que contiene archivos de configuración (parámetros del modelo, instrucción de sistema).
*   `bot-env/`: Directorio del entorno virtual de Python.
*   `.env`: Archivo para variables de entorno sensibles (excluido de Git).
*   `.gitignore`: Define los archivos y directorios a ignorar por Git.
*   `requirements.txt`: Lista de dependencias del proyecto.
*   `test.py`: (Detectado) Archivo para pruebas o experimentación.

## NOTA:  

*   Si quieres ejecutar este agente desde cualquier parte en la terminal, crea un archivo .bat como este:  
    ```bash
    @echo off

    call *ruta absoluta al script de activación del entorno virtual* 
    python *ruta absoluta al archivo main.py*
    ```  
    Y guardalo dentro de la carpeta C:\Windows (requiere permisos de administrador) con un nombre fácil ej: *kurisu*. Ahora puedes llamar al agente escribiendo el nombre del script .bat en la terminal
---