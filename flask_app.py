from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from collections import defaultdict

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return jsonify({'mensaje': 'No se ha cargado ningún archivo.'}), 400

    archivo = request.files['archivo']

    if archivo and archivo.filename.endswith('.xml'):
        contenido = archivo.read().decode('utf-8')

        try:
            root = ET.fromstring(contenido)
        except ET.ParseError as e:
            return jsonify({'mensaje': f'Error al procesar el archivo XML: {e}'}), 400

        contador = contar_ventas_por_departamento(root)
        resultados_xml = crear_xml_resultados(contador)

        # Guardar el XML en un archivo para referencia
        filename = 'resultados_ventas.xml'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(resultados_xml)

        # Devolver el contenido XML directamente
        return jsonify({'mensaje': 'Archivo procesado con éxito.', 'resultados': resultados_xml}), 200

    return jsonify({'mensaje': 'Tipo de archivo no válido, se espera un archivo XML.'}), 400

def contar_ventas_por_departamento(root):
    contador = defaultdict(int)
    for venta in root.findall('.//venta'):
        departamento = venta.get('departamento')
        contador[departamento] += 1
    return contador

def crear_xml_resultados(contador):
    xml_resultados = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n  <departamentos>\n'
    for departamento, cantidad in contador.items():
        xml_resultados += f'    <{departamento}>\n'
        xml_resultados += f'      <cantidadVentas>{cantidad}</cantidadVentas>\n'
        xml_resultados += f'    </{departamento}>\n'
    xml_resultados += '  </departamentos>\n</resultados>'
    return xml_resultados

if __name__ == '__main__':
    app.run(debug=True, port=5000)