from django.shortcuts import render
from django.http import HttpResponse
import requests

def cargar_datos(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            if archivo.size > 0:
                # URL de tu backend Flask
                url = 'http://127.0.0.1:5000/upload'
                files = {'archivo': (archivo.name, archivo.read())}
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    # Solo guardar el archivo, sin mostrarlo
                    data = response.json()
                    mensaje = data['mensaje']
                    resultados = data['resultados']  # Obtenemos el XML generado
                    # Guardar el XML en la sesión
                    request.session['resultados_xml'] = resultados
                    return render(request, 'cargar_datos.html', {'mensaje': mensaje})
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
    return render(request, 'ver_grafico.html')

def datos_estudiante(request):
    return render(request, 'datos_estudiante.html')

# Inicia el servidor Flask cuando se ejecute el script
if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, flask_app)