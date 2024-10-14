from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return jsonify({'mensaje': 'No se ha cargado ningún archivo.'}), 400

    archivo = request.files['archivo']

    # Verificar si el archivo tiene contenido
    if archivo and archivo.filename.endswith('.xml'):
        # Leer el archivo y procesar su contenido
        contenido = archivo.read().decode('utf-8')

        # Imprimir el contenido del archivo en la consola
        print(f'Contenido del archivo:\n{contenido}')

        # Procesar el contenido XML
        try:
            root = ET.fromstring(contenido)
            print("Archivo XML procesado con éxito.")
        except ET.ParseError as e:
            return jsonify({'mensaje': f'Error al procesar el archivo XML: {e}'}), 400

        return jsonify({'mensaje': 'Archivo cargado y procesado con éxito.'}), 200

    return jsonify({'mensaje': 'Tipo de archivo no válido, se espera un archivo XML.'}), 400

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)