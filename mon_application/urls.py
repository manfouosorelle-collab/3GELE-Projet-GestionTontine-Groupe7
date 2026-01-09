
from django.urls import path,include
from django.urls import *
from .views import *
from .models import *
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',connexion,name='connexion'),
    path('inscription',inscription,name='inscription'),
    path('home', home ,name='home'),
    path('home2', home2 ,name='home2'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('member_dashboard', member_dashboard, name='member_dashboard'),
    path('liste_membres', liste_membres, name='liste_membres'),
    path('liste_membres2', liste_membres2, name='liste_membres2'),
    path('ajouter_membre', ajouter_membre, name='ajouter_membre'),
    path('ajouter_membre/', ajouter_membre, name='ajouter_membre'),
    path('modifier_membre/<int:idmembre>/', modifier_membre, name='modifier_membre'),
    path('supprimer_membre/<int:idmembre>/', supprimer_membre, name='supprimer_membre'),

    path('liste_tontine', liste_tontine, name='liste_tontine'),
    path('liste_tontine2', liste_tontine2, name='liste_tontine2'),
    path('ajouter_tontine', ajouter_tontine, name='ajouter_tontine'),
    path('ajouter_membre__tontine', ajouter_membre_tontine, name='ajouter_membre_tontine'),
    path('modifier_tontine/<int:idTontines>/', modifier_tontine, name='modifier_tontine'),
    path('supprimer_tontine/<int:idTontines>/', supprimer_tontine, name='supprimer_tontine'),
    path('souscrire_tontine/<int:idTontines>/', souscrire_tontine, name='souscrire_tontine'),
    path('voir_membres_tontines/<int:idTontines>/', voir_membres_tontines, name='voir_membres_tontines'),
    path('tableau_de_bord/', tableau_de_bord, name='tableau_de_bord'),
    path('tableau_de_bord2/', tableau_de_bord2, name='tableau_de_bord2'),



    
    
    path('demande_pret/', demande_pret, name='demande_pret'),
    path('gestion_demandes/', gestion_demandes, name='gestion_demandes'),
    path('valider_demande/<int:idpret>/', valider_demande, name='valider_demande'),
    path('refuser_demande/<int:idpret>/', refuser_demande, name='refuser_demande'),
    path('liste_prets/', liste_prets, name='liste_prets'),
    path('effectuer_remboursement/', effectuer_remboursement, name='effectuer_remboursement'),
    path('effectuer_remboursement2/', effectuer_remboursement2, name='effectuer_remboursement2'),


    path('effectuer_don', effectuer_don, name='effectuer_don'),
    path('liste_dons_connecte',liste_dons_connecte, name='liste_dons_connecte'),
    path('liste_tous_les_dons', liste_tous_les_dons, name='liste_tous_les_dons'),
    
    


    path('statistiques_view/', statistiques_view, name='statistiques_view'),
    path('statistiques_view2/', statistiques_view2, name='statistiques_view2'),


    
      
]
   
    
    
    



