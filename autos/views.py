import base64
from django.shortcuts import render
from django.http import HttpResponse
import requests
from werkzeug import run_simple
import flask_app

def cargar_datos(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            print(f'Archivo cargado: {archivo.name}, tamaño: {archivo.size} bytes')

            if archivo.size > 0:
                # URL de tu backend Flask
                url = 'http://127.0.0.1:5000/upload'  
                files = {'archivo': (archivo.name, archivo.read())}
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    data = response.json()
                    print(f'Respuesta de Flask: {data}')  # <-- Agrega esta línea para depuración
                    resultados = data.get('resultados')  # Usa .get() en lugar de acceder directamente
                    
                    # Almacenar los resultados en la sesión
                    request.session['resultados_xml'] = resultados
                    
                    if resultados:
                        return render(request, 'cargar_datos.html', {'mensaje': resultados})
                    else:
                        return render(request, 'cargar_datos.html', {'mensaje': 'No se encontraron resultados.'})
                else:
                    mensaje = response.json().get('mensaje', 'Error desconocido.')
                    return render(request, 'cargar_datos.html', {'mensaje': mensaje})
            else:
                return render(request, 'cargar_datos.html', {'mensaje': 'El archivo está vacío.'})
        else:
            return render(request, 'cargar_datos.html', {'mensaje': 'No se ha cargado ningún archivo.'})

    return render(request, 'cargar_datos.html')

def procesar_datos(request):
    if request.method == 'POST':
        # Recuperamos el XML almacenado en la sesión
        datos_xml = request.session.get('resultados_xml', None)
        return render(request, 'procesar_datos.html', {'datos_xml': datos_xml})
    
    # Si no es POST, mostramos la página sin datos
    return render(request, 'procesar_datos.html')

def ver_grafico(request):
    # Solicitar el gráfico a Flask
    url = 'http://127.0.0.1:5000/grafico'
    response = requests.get(url)

    if response.status_code == 200:
        # Leer la imagen en bytes y codificarla en base64
        imagen_base64 = base64.b64encode(response.content).decode('utf-8')
        return render(request, 'ver_grafico.html', {'imagen': imagen_base64})
    else:
        return render(request, 'ver_grafico.html', {'mensaje': 'No se pudo cargar el gráfico.'})

def datos_estudiante(request):
    return render(request, 'datos_estudiante.html')

# Inicia el servidor Flask cuando se ejecute el script
if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, flask_app)