from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from collections import defaultdict

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

        # Contar ventas por departamento
        contador = contar_ventas_por_departamento(root)

        # Crear el XML de resultados con la estructura correcta
        resultados_xml = crear_xml_resultados(contador)

        # Guardar el XML en un archivo
        filename = 'resultados_ventas.xml'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(resultados_xml)

        # Imprimir el archivo XML creado
        print(f'Contenido del archivo creado:\n{resultados_xml}')

        return jsonify({'mensaje': 'Archivo cargado y procesado con éxito.'}), 200

    return jsonify({'mensaje': 'Tipo de archivo no válido, se espera un archivo XML.'}), 400

def contar_ventas_por_departamento(root):
    contador = defaultdict(int)  # Usamos un defaultdict para contar las ventas

    for venta in root.findall('.//venta'):
        departamento = venta.get('departamento')
        contador[departamento] += 1  # Aumentar el conteo del departamento

    return contador

def crear_xml_resultados(contador):
    # Iniciar la estructura XML manualmente
    xml_resultados = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n  <departamentos>\n'

    for departamento, cantidad in contador.items():
        # Agregar el departamento como etiqueta y la cantidad de ventas como contenido
        xml_resultados += f'    <{departamento}>\n'
        xml_resultados += f'      <cantidadVentas>{cantidad}</cantidadVentas>\n'
        xml_resultados += f'    </{departamento}>\n'

    # Cerrar las etiquetas del XML
    xml_resultados += '  </departamentos>\n</resultados>'

    return xml_resultados

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)