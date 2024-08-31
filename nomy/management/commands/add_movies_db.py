from django.core.management.base import BaseCommand
from nomy.models import Nomy
import os
import json

class Command(BaseCommand):
    help = 'Load nomys from nomy_descriptions.json into the Nomy model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola esta ubicada en la carpeta DjangoProjectBase.
        #El path del archivo movie_descriptions con respecto a DjangiProjectsBase seria la carpeta anterior
        json_file_path = 'nomy/management/commands/nomys.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            nomys = json.load(file)

        # Add products to the database
        for i in range(100):
            nomy = nomys[i]
            exist = Nomy.objects.filter(title = nomy['title']).first() #Se asegura que la pelicula no exista en la base de datos
            if not exist:
                Nomy.objects.create(title = nomy['title'],
                                    image = 'media/movie/images/default.jpg',
                                    genre = nomy['genre'],
                                    year = nomy['year'])
                

        #self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} products to the database'))