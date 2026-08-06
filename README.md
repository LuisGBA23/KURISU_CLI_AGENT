# Kurisu CLI Agent

Este repositorio contiene un agente de inteligencia artificial interactivo basado en línea de comandos, diseñado para interactuar con modelos de lenguaje avanzados de Google (Gemini). El agente está personalizado para ofrecer asistencia en tareas técnicas, gestión de archivos, ejecución de comandos del sistema y control de versiones Git, todo ello manteniendo un contexto conversacional persistente.

## Características Principales

*   **Interacción Conversacional:** Permite una comunicación fluida con el modelo de lenguaje, manteniendo el contexto de la conversación a través del historial.
*   **Ejecución de Comandos del Sistema:** Capacidad para ejecutar comandos de shell directamente en el sistema operativo, con mecanismos de seguridad para comandos que requieren privilegios elevados (`sudo`).
*   **Gestión y Edición de Archivos:** Herramientas para leer, escribir y realizar ediciones avanzadas en archivos (añadir contenido, insertar/borrar líneas, reemplazar texto).
*   **Control de Versiones Git:** Integración para realizar operaciones de `commit` en repositorios Git, facilitando la gestión del código fuente.
*   **Personalidad Definida:** Configurado con instrucciones de sistema para guiar el comportamiento y tono del agente.
*   **Gestión de Claves API:** Soporte para múltiples claves API de Gemini.
*   **Entorno Aislado:** Utiliza un entorno virtual de Python (`venv`) para gestionar las dependencias del proyecto de forma limpia y aislada.

## Tecnologías Utilizadas

*   **Python 3.x**
*   **Google Gemini API:** Para la interacción con modelos de lenguaje avanzados.
*   **`python-dotenv`:** Para la gestión segura de variables de entorno (claves API).
*   **`colorama`:** Para estilizar la salida de la terminal.
*   **`subprocess`:** Para la ejecución de comandos del sistema.
*   **`BeautifulSoup4` y `requests`:** (Detectadas como dependencias, útiles para futuras capacidades de web scraping/búsqueda).
*   **`selenium` y `webdriver_manager`:** (Detectadas como dependencias, útiles para automatización web).

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
    Crea un archivo `.env` en la raíz del directorio del proyecto y añade tus claves API de Google Gemini.
    ```
    # .env
    GEMINI_KEYS="TU_CLAVE_API_1,TU_CLAVE_API_2" # Puedes añadir múltiples claves separadas por comas
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
*   `Chats_history.py`: Módulo para la carga y guardado del historial de conversaciones.
*   `Utilities.py`: Funciones de utilidad generales y auxiliares.
*   `configs/`: Directorio que contiene archivos de configuración (parámetros del modelo, instrucción de sistema).
*   `bot-env/`: Directorio del entorno virtual de Python.
*   `.env`: Archivo para variables de entorno sensibles (excluido de Git).
*   `.gitignore`: Define los archivos y directorios a ignorar por Git.
*   `requirements.txt`: Lista de dependencias del proyecto.
*   `test.py`: (Detectado) Archivo para pruebas o experimentación.

---