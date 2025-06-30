# 🚗 API - Sistema de Control Vehicular – USMP 🚗
## 🚀 Tecnologías y Herramientas Utilizadas

- Lenguaje: Python 3.11+

- Frontend: HTML + JS (carpeta client/)

- Backend/API: Flask, Flask-CORS

- Reconocimiento de placas: API de PlateRecognizer

- Base de datos: PostgreSQL

- Interfaz previa: PySimpleGUI + OpenCV

`Librerías:`
```python
pip install flask pandas pillow requests flask-cors psycopg2
```
## 🔧 Instrucciones de Instalación

Crear un entorno virtual:
```python
python3 -m venv venv
source venv/bin/activate
```
Instalar las dependencias:
```python
pip install flask pandas pillow requests flask-cors psycopg2
```
Ejecutar la API:
```python
python app.py
```
Acceder a la web desde el navegador:
`http://127.0.0.1:5000/`

## 📄 Estructura del JSON para Gestión de Placas
`{
  "numero_placa": "ABC123",
  "estado": "ACTIVO",
  "accion": "insertar"
}`

`Acciones disponibles: insertar, actualizar, eliminar.`
## 📊 Integración con PostgreSQL (opcional)

Configuración para conexión a PostgreSQL:
```python
PG_HOST = 'localhost'
PG_PORT = '5432'
PG_DBNAME = 'nombre_base_datos'
PG_USER = 'tu_usuario'
PG_PASSWORD = 'tu_contraseña'
```
Uso en API para insertar, actualizar o eliminar:
```python
@app.route('/api/manage-plate', methods=['POST'])
def manage_plate():
    ...
```
## 🚪 Estado del Proyecto

✅ Versión funcional API REST.

🔄 En desarrollo APK Android con Android Studio.



