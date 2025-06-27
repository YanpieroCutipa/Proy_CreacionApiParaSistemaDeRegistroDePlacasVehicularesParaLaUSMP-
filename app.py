from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import base64
import re
from io import BytesIO
from PIL import Image
import requests
import csv
import os

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde otros dominios 

# Archivos usados para la base de datos de placas y para guardar registros
DB_FILE = 'placas_autorizadas.csv'
SAVE_FILE = 'save.csv'

# Token de autenticación para la API de reconocimiento de placas
API_TOKEN = 'b3d98b5c20a27f8c9e6b4adf74fc7c85e49213f2'

# Carga el archivo CSV de placas autorizadas y las convierte en un diccionario
def cargar_placas_autorizadas():
    try:
        df = pd.read_csv(DB_FILE)
        return dict(zip(df['numero_placa'].str.upper(), df['estado'].str.upper()))
    except FileNotFoundError:
        return {}

# Envía la imagen a la API externa y obtiene la información de la placa
def leer_placa_bytes(image_bytes):
    regions = ['us', 'mx']
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=regions),
        files={'upload': image_bytes},
        headers={'Authorization': f'Token {API_TOKEN}'}
    )
    return response.json()

# Ruta principal para procesar la imagen base64 y devolver información de la placa
@app.route('/api/read-plate', methods=['POST'])
def read_plate():
    data = request.get_json()
    if not data or 'image_base64' not in data:
        return jsonify({'error': 'Campo image_base64 requerido'}), 400

    try:
        # Limpia y decodifica la imagen base64
        base64_str = re.sub('^data:image/[^;]+;base64,', '', data['image_base64'])
        image_bytes = BytesIO(base64.b64decode(base64_str))
        image_bytes.seek(0)

        # Procesa la imagen con la API y carga las placas autorizadas
        response_data = leer_placa_bytes(image_bytes)
        placas_autorizadas = cargar_placas_autorizadas()

        resultados = []
        for result in response_data.get('results', []):
            plate = result['plate'].upper()
            estado = placas_autorizadas.get(plate, 'NO ENCONTRADO')  # Verifica si la placa está autorizada

            resultado = {
                'numero_placa': plate,
                'estado': estado,
                'score': result.get('score'),
                'dscore': result.get('dscore')
            }
            resultados.append(resultado)

            # Guarda un registro de cada lectura en un archivo CSV
            with open(SAVE_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['fecha', 'numero_placa', 'precision', 'dscore'])
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow({
                    'fecha': datetime.now().strftime('%x %X'),
                    'numero_placa': plate,
                    'precision': result.get('score'),
                    'dscore': result.get('dscore')
                })

        return jsonify({'resultados': resultados})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Sirve el archivo index.html de la carpeta client (frontend)
@app.route('/')
def serve_index():
    return send_from_directory('client', 'index.html')

# Sirve archivos estáticos de la carpeta client (JS, CSS, imágenes)
@app.route('/client/<path:path>')
def serve_static(path):
    return send_from_directory('client', path)

# Inicia la aplicación Flask en modo debug
if __name__ == '__main__':
    app.run(debug=True)
