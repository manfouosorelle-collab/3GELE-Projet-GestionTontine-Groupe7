from django.core.management.base import BaseCommand
from mon_application.models import Tontines  # Remplacez par le nom de votre application

class Command(BaseCommand):
    help = 'Initialiser les tontines avec des montants par défaut'

    def handle(self, *args, **kwargs):
        tontine_data = [  # Renommé pour éviter la confusion
            ('presence', 'Tontine de Présence', 1000),
            ('epargne', 'Tontine d_epargne', 2500),
            ('solidarite', 'Tontine de solidarite', 3000),
            ('rotative', 'Tontine rotative', 2000),
        ]
        
        for typeTontine, nom, montant in tontine_data:
            Tontines.objects.get_or_create(
                typeTontine=typeTontine,
                defaults={'montant': montant}
            )
        
        self.stdout.write(self.style.SUCCESS('Tontines initialisées avec succès !'))