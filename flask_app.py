from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from collections import defaultdict
from xml.dom import minidom  # Importamos minidom para formatear el XML
import os

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

        # Crear el XML de resultados
        resultados_xml = crear_xml_resultados(contador)

        # Guardar el XML en un archivo formateado
        try:
            filename = 'resultados_ventas.xml'
            guardar_xml_en_archivo(resultados_xml, filename)
            print("Archivo XML guardado como 'resultados_ventas.xml'.")

            # Imprimir el contenido del archivo XML creado
            with open(filename, 'r', encoding='utf-8') as file:
                print(f'Contenido del archivo guardado:\n{file.read()}')

        except Exception as e:
            return jsonify({'mensaje': f'Error al guardar el archivo XML: {e}'}), 500

        return jsonify({'mensaje': 'Archivo cargado y procesado con éxito.'}), 200

    return jsonify({'mensaje': 'Tipo de archivo no válido, se espera un archivo XML.'}), 400

def contar_ventas_por_departamento(root):
    contador = defaultdict(int)  # Usamos un defaultdict para contar las ventas

    for venta in root.findall('.//venta'):
        departamento = venta.get('departamento')
        contador[departamento] += 1  # Aumentar el conteo del departamento

    return contador

def crear_xml_resultados(contador):
    resultados = ET.Element('resultados')
    departamentos = ET.SubElement(resultados, 'departamentos')

    for departamento, cantidad in contador.items():
        depto_elem = ET.SubElement(departamentos, 'departamento', nombre=departamento)
        
        # Crear el elemento cantidadVentas
        cantidad_elem = ET.SubElement(depto_elem, 'cantidadVentas')
        cantidad_elem.text = str(cantidad)  # Asignamos la cantidad

    return resultados

def guardar_xml_en_archivo(xml_element, filename):
    # Guardar el XML en un archivo de forma legible
    xml_str = ET.tostring(xml_element, encoding='utf-8', xml_declaration=True).decode('utf-8')
    pretty_xml = minidom.parseString(xml_str)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(pretty_xml.toprettyxml(indent="  "))  # Escribimos el XML con indentación

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)