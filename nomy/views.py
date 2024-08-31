import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse

from .models import Nomy

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Samuel Gutierrez'})
    searchTerm = request.GET.get('searchNomy')
    if searchTerm:
        nomys = Nomy.objects.filter(title__icontains=searchTerm)
    else:    
        nomys = Nomy.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'nomys': nomys})

def about(request):
    #return HttpResponse('<h1>About page</h1>')
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las peliculas
    all_nomys = Nomy.objects.all()

    # Crear un diccionario para almacenar la cantidad de peliculas por año
    nomy_counts_by_year = {}

    # Filtrar las peliculas por año y contar la cantidad de peliculas por año
    for nomy in all_nomys:
        year = nomy.year if nomy.year else "None"
        if year in nomy_counts_by_year:
            nomy_counts_by_year[year] += 1
        else:
            nomy_counts_by_year[year] = 1

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(nomy_counts_by_year))

    # Crear la grafica de barras
    plt.bar(bar_positions, nomy_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la grafica
    plt.title('Nomys per year')
    plt.xlabel('Year')
    plt.ylabel('Number of nomys')
    plt.xticks(bar_positions, nomy_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la grafica en un objetivo BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la grafica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png)
    graphic_year = graphic_year.decode('utf-8')

    # Crear un diccionario para almacenar la cantidad de peliculas por genero
    nomy_counts_by_genre = {}

    # Filtrar las peliculas por genero y contar la cantidad de peliculas por genero
    for nomy in all_nomys:
        genre = nomy.genre if nomy.genre else "None"
        if genre in nomy_counts_by_genre:
            nomy_counts_by_genre[genre] += 1
        else:
            nomy_counts_by_genre[genre] = 1

    # Posiciones de las barras
    bar_positions = range(len(nomy_counts_by_genre))

    # Crear la grafica de barras
    plt.bar(bar_positions, nomy_counts_by_genre.values(), width=bar_width, align='center')

    # Personalizar la grafica
    plt.title('Nomys per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of nomys')
    plt.xticks(bar_positions, nomy_counts_by_genre.keys(), rotation=90)

    # Guardar la grafica en un objetivo BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la grafica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')

    # Reenderizar la plantilla statistics.html con la grafica
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})