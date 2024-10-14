from flask import Flask, request, jsonify, send_file
import xml.etree.ElementTree as ET
from collections import defaultdict
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Variable global para almacenar los resultados
ventas_por_departamento = None

@app.route('/upload', methods=['POST'])
def upload_file():
    global ventas_por_departamento  # Usamos la variable global

    if 'archivo' not in request.files:
        return jsonify({'mensaje': 'No se ha cargado ningún archivo.'}), 400

    archivo = request.files['archivo']

    # Verificar si el archivo tiene contenido
    if archivo and archivo.filename.endswith('.xml'):
        # Leer el archivo y procesar su contenido
        contenido = archivo.read().decode('utf-8')

        # Procesar el contenido XML
        try:
            root = ET.fromstring(contenido)
            print("Archivo XML procesado con éxito.")
        except ET.ParseError as e:
            return jsonify({'mensaje': f'Error al procesar el archivo XML: {e}'}), 400

        # Contar ventas por departamento y guardar en la variable global
        ventas_por_departamento = contar_ventas_por_departamento(root)

        return jsonify({'mensaje': 'Archivo cargado y procesado con éxito.'}), 200

    return jsonify({'mensaje': 'Tipo de archivo no válido, se espera un archivo XML.'}), 400

def contar_ventas_por_departamento(root):
    contador = defaultdict(int)
    for venta in root.findall('.//venta'):
        departamento = venta.get('departamento')
        contador[departamento] += 1
    return contador

@app.route('/grafico', methods=['GET'])
def generar_grafico():
    global ventas_por_departamento  # Acceder a la variable global

    if ventas_por_departamento is None:
        return jsonify({'mensaje': 'No hay datos de ventas disponibles.'}), 400

    # Generar gráfico de pastel
    departamentos = list(ventas_por_departamento.keys())
    ventas = list(ventas_por_departamento.values())

    fig, ax = plt.subplots()
    ax.pie(ventas, labels=departamentos, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Para que sea un círculo.

    # Guardar la gráfica en un objeto de memoria (buffer)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Retornar la gráfica como un archivo de imagen PNG
    return send_file(buf, mimetype='image/png')

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)