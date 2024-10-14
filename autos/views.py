from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import os
import requests

def cargar_datos(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            # Imprimir el nombre y tamaño del archivo en la consola
            print(f'Archivo cargado: {archivo.name}, tamaño: {archivo.size} bytes')

            # Comprobar si el archivo tiene contenido
            if archivo.size > 0:
                # Imprimir el directorio del archivo en la consola
                directorio_archivo = os.path.abspath(archivo.name)
                print(f'Directorio del archivo: {directorio_archivo}')



            else:
                print('El archivo está vacío.')  # Mensaje en consola si el archivo está vacío
                return render(request, 'cargar_datos.html', {'mensaje': 'El archivo está vacío.'})

        else:
            print('No se ha cargado ningún archivo.')  # Mensaje en consola si no hay archivo
            return render(request, 'cargar_datos.html', {'mensaje': 'No se ha cargado ningún archivo.'})

    return render(request, 'cargar_datos.html')

def procesar_datos(request):
    return render(request, 'procesar_datos.html')

def ver_grafico(request):
    return render(request, 'ver_grafico.html')

def datos_estudiante(request):
    return render(request, 'datos_estudiante.html')