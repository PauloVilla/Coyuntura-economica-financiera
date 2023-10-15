
# Coyuntura-economica-financiera
Dashboard de Coyuntura Económica y Financiera: Datos actualizados de Alpha Advantage y Yahoo Finance junto con noticias destacadas, todo en una interfaz Streamlit concisa y atractiva en Python.

Para que funcione, el usuario debe tener de manera local, en la misma ubicación de la carpeta base, un archivo llamado config.py con la API_KEY de Alpha Vantage, bajo el nombre de variable `api_key`

# Instalación
## 1. Usando `virtualenv`:

### Instalación:
Si aún no tienes `virtualenv` instalado, puedes hacerlo con pip:
```
pip install virtualenv
```

### Creación de un entorno virtual:
```
virtualenv nombre_del_entorno
```
Esto creará un directorio llamado `nombre_del_entorno` en tu directorio actual que contendrá un entorno virtual de Python.

### Activación del entorno virtual:

- **Windows**:
```
nombre_del_entorno\Scripts\activate
```

- **macOS y Linux**:
```
source nombre_del_entorno/bin/activate
```

Una vez activado, cualquier paquete que instales con pip se instalará en este entorno virtual y no afectará a tu instalación global de Python.

### Instalación de dependencias:
Si tienes un archivo `requirements.txt`, puedes instalar todas las dependencias listadas en él con:
```
pip install -r requirements.txt
```

### Desactivación del entorno virtual:
```
deactivate
```

## 2. Usando `pipenv`:

### Instalación:
Si aún no tienes `pipenv` instalado, puedes hacerlo con pip:
```
pip install pipenv
```

### Creación de un entorno virtual y instalación de dependencias:
En lugar de crear un entorno virtual y luego instalar dependencias por separado como con `virtualenv`, `pipenv` combina ambos pasos. Navega al directorio donde se encuentra tu `requirements.txt` y ejecuta:
```
pipenv install --ignore-pipfile
```

Esto creará un entorno virtual (si no existe) y luego instalará las dependencias listadas en `requirements.txt`. Nota que la opción `--ignore-pipfile` es para asegurarnos de que se utilice `requirements.txt` y no un `Pipfile` existente.

### Activación del entorno virtual:
```
pipenv shell
```

## Ejecución de la Aplicación Streamlit

Streamlit es una herramienta increíble que te permite convertir fácilmente tus scripts de Python en aplicaciones web interactivas sin la necesidad de tener conocimientos de desarrollo web.

### Correr la Aplicación:

Una vez que tengas `streamlit` instalado y estés en el directorio que contiene `app.py`, puedes ejecutar la aplicación con el siguiente comando:

```bash
streamlit run app.py
```

Después de ejecutar el comando, Streamlit te mostrará una URL en tu terminal. Normalmente, es algo como `http://localhost:8501/`. Abre esa URL en tu navegador para ver y interactuar con tu aplicación.

### Opciones Adicionales:

Si quieres conocer más sobre las opciones que ofrece `streamlit run`, puedes usar:

```bash
streamlit run --help
```

### Documentación del proyecto

La documentación de este proyecto la puedes encontrar en el archivo `Visualizaciones_Dashboard.ipynb`. Este es un notebook de Jupyter que puedes visualizar mediante: 

```bash
jupyter lab Visualizaciones_Dashboard.ipynb
```
