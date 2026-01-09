from django.shortcuts import render

# views.py
from django.contrib.auth import * 
from django.shortcuts import redirect, render
from .models import *
from django.forms import *
from .forms import connexionForm
from django.shortcuts import render, redirect
from .models import User  # Assurez-vous d'importer votre modèle utilisateur
from .forms import membreForm
from .forms import*
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import membre
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import membre  # Assurez-vous d'importer le modèle






def connexion(request):
    return render(request,'connexion.html')
def inscription(request):
    return render(request,'inscription.html')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def member_dashboard(request):
    return render(request,'member_dashboard.html')
def home(request):
    return render(request,'home.html')
def home2(request):
    return render(request,'home2.html')
def liste_membres(request):
    return render(request,'liste_membres.html')
def ajouter_membre(request):
    return render(request,'ajouter_membre.html')
def supprimer_membre(request):
    return render(request,'supprimer_membre.html')
def modifier_membre(request):
    return render(request,'modifier_membre.html')
def liste_tontine(request):
    return render(request,'liste_tontine.html')
def valider_demande(request):
    return render(request,'valider_demande.html')






def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentifier l'utilisateur et créer une session
            login(request, user)  # Cela crée une session pour l'utilisateur

            # Récupérer le membre associé
            try:
                membre_instance = membre.objects.get(user=user)  # Assurez-vous d'utiliser la bonne classe
                request.session['membre_id'] = membre_instance.idmembre  # Enregistrer l'ID du membre dans la session

                if membre_instance.role == 'admin':
                    return redirect('admin_dashboard')  # Redirection vers la page admin
                else:
                    return redirect('member_dashboard')  # Redirection vers la page membre
            except membre.DoesNotExist:
                messages.error(request, 'Utilisateur non trouvé.')
                return redirect('inscription')  # Rediriger vers l'inscription
        else:
            messages.error(request, 'Identifiants invalides. Création d\'un nouveau compte.')
            return redirect('inscription')  # Rediriger vers l'inscription

    return render(request, 'connexion.html')





def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
       
        nom = request.POST['nom']
        email = request.POST['email']
        
        prenom = request.POST['prenom']
        anneeEntree = request.POST['anneeEntree']
        anneeNais = request.POST.get('anneeNais')
        telephone = request.POST['telephone']
        actif = request.POST['actif']
        user = authenticate(request, username=username, password=password)
        

        role = request.POST.get('role')

        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # Créer une instance de membre
        new_member = membre(
            nom=nom,
            email=email,
            password=make_password(password),  # Hash le mot de passe
            prenom=prenom,
            anneeEntree=anneeEntree,
            anneeNais=anneeNais,
            telephone= telephone,
            actif= actif,
            role=role,
            user=user
        )
        new_member.save()
        messages.success(request, 'Inscription réussie ! Vous pouvez vous connecter.')
        return redirect('connexion')  # Redirection vers la page de connexion

    return render(request, 'inscription.html')



from .models import membre
from .forms import membreForm  # Assurez-vous d'avoir un formulaire pour le modèle membre

from django.shortcuts import render, get_object_or_404, redirect
from .models import membre
from .forms import membreForm  # Assurez-vous de créer un formulaire pour Membre.

def liste_membres(request):
    membres = membre.objects.all()
    return render(request, 'liste_membres.html', {'membres': membres})

def liste_membres2(request):
    membres = membre.objects.all()
    return render(request, 'liste_membres2.html', {'membres': membres})

def ajouter_membre(request):
    if request.method == 'POST':
        form = membreForm(request.POST)
        if form.is_valid():
            
            nom = request.POST['nom']
            email = request.POST['email']
            password = request.POST.get('password')  # Mot de passe d'origine 
            prenom = request.POST['prenom']
            anneeEntree = request.POST['anneeEntree']
            anneeNais = request.POST.get('anneeNais')
            telephone = request.POST['telephone']
            actif = request.POST['actif']
            

            role = request.POST.get('role')

            # Créer un nouvel utilisateur
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()

            # Créer une instance de membre
            new_member = membre(
                nom=nom,
                email=email,
                password=make_password(password),  # Hash le mot de passe
                prenom=prenom,
                anneeEntree=anneeEntree,
                anneeNais=anneeNais,
                telephone= telephone,
                actif= actif,
                role=role,
                user=user
            )
            new_member.save()
        
                
                # Mot de passe d'origine             
                
            form = form.save(commit=False)
            
            form.save()

            
            return redirect('liste_membres')
    else:
        form = membreForm()
    return render(request, 'ajouter_membre.html', {'form': form})




from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import membre

def modifier_membre(request, idmembre):
    membre_instance = get_object_or_404(membre, idmembre=idmembre)

    if request.method == 'POST':
        membre_instance.nom = request.POST.get('nom')
        membre_instance.email = request.POST.get('email')
        membre_instance.prenom = request.POST.get('prenom')
        membre_instance.anneeEntree = request.POST.get('anneeEntree')
        membre_instance.anneeNais = request.POST.get('anneeNais')
        membre_instance.telephone = request.POST.get('telephone')
        membre_instance.actif = request.POST.get('actif')
        membre_instance.role = request.POST.get('role')

        membre_instance.save()
        messages.success(request, 'Membre modifié avec succès.')
        return redirect('member_dashboard')  # Redirection après modification

    context = {
        'membre': membre_instance
    }
    return render(request, 'modifier_membre.html', context)



def supprimer_membre(request, idmembre):
    membre_instance = get_object_or_404(membre, idmembre=idmembre)

    if request.method == 'POST':
        membre_instance.delete()
        messages.success(request, 'Membre supprimé avec succès.')
        return redirect('liste_membres')  # Redirection après suppression

    context = {
        'membre': membre_instance
    }
    return render(request, 'supprimer_membre.html', context)


# Tontine

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tontines, Souscription, membre


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tontines, Souscription
from .forms import TontineForm  # Assurez-vous d'avoir créé ce formulaire



def liste_tontine(request):
    tontines = Tontines.objects.all()
    return render(request, 'liste_tontine.html', {'tontines': tontines})

def liste_tontine2(request):
    tontines = Tontines.objects.all()
    return render(request, 'liste_tontine2.html', {'tontines': tontines})



def ajouter_membre_tontine(request):
    if request.method == 'POST':
        form = AjouterMembreTontineForm(request.POST)
        if form.is_valid():
            membre_obj = form.cleaned_data['membre']
            tontine_obj = form.cleaned_data['tontine']

            # Vérifie si la souscription existe déjà
            if not Souscription.objects.filter(membre=membre_obj, tontine=tontine_obj).exists():
                Souscription.objects.create(membre=membre_obj, tontine=tontine_obj)
            return redirect('liste_tontine')  # Redirige vers la page appropriée
    else:
        form = AjouterMembreTontineForm()
    
    return render(request, 'ajouter_membre_tontine.html', {'form': form})



def ajouter_tontine(request):
    if request.method == 'POST':
        form = TontineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tontine ajoutée avec succès!')
            return redirect('liste_tontine')
    else:
        form = TontineForm()
    return render(request, 'ajouter_tontine.html', {'form': form})


def modifier_tontine(request, idTontines):
    tontine = get_object_or_404(Tontines, idTontines=idTontines)

    if request.method == 'POST':
        tontine.typeTontine = request.POST.get('typeTontine')
        tontine.montant = request.POST.get('montant')
        tontine.save()
        messages.success(request, 'Tontine modifiée avec succès.')
        return redirect('liste_tontine')
    
    

    return render(request, 'modifier_tontine.html', {'tontine': tontine})








def supprimer_tontine(request, idTontines):
    tontine = get_object_or_404(Tontines, idTontines=idTontines)
    if request.method == 'POST':
        tontine.delete()
        messages.success(request, 'Tontine supprimée avec succès!')
        return redirect('liste_tontines')
    return render(request, 'supprimer_tontine.html', {'tontine': tontine})


def souscrire_tontine(request, idTontines):
    tontine = get_object_or_404(Tontines, idTontines=idTontines)

    if request.method == 'POST':
       
        membre = request.user.membre  # Récupérer l'instance de Membre liée à l'utilisateur connecté

        # Créer la souscription
        souscription = Souscription(tontine=tontine, membre=membre)
        souscription.save()  # Enregistrer dans la base de données

        messages.success(request, "Souscription réussie !")  # Message de succès
        return redirect('liste_tontine')  # Rediriger vers la liste des tontines

    return render(request, 'souscrire_tontine.html', {'tontine': tontine})



# views.py
'''
from .models import Tontines, Souscription, membre
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

@login_required
def voir_membres_tontine(request, idTontines):
    tontine = get_object_or_404(Tontines, idTontines=idTontines)
    membres_souscrits = Souscription.objects.filter(tontine=tontine)

    if request.method == 'POST':
        membre_courant = request.user.membre
        # Vérifie si déjà souscrit
        if not Souscription.objects.filter(tontine=tontine, membre=membre_courant).exists():
            Souscription.objects.create(tontine=tontine, membre=membre_courant)
            messages.success(request, "Souscription réussie à la tontine.")
        else:
            messages.info(request, "Vous êtes déjà souscrit à cette tontine.")
        return redirect('liste_tontine')

    return render(request, 'voir_membres_tontine.html', {
        'tontine': tontine,
        'membres_souscrits': membres_souscrits
    })'''


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Tontines, Souscription

def voir_membres_tontines(request, idTontines):
    tontine = get_object_or_404(Tontines, pk=idTontines)
    souscriptions = Souscription.objects.filter(tontine=tontine).select_related('membre')
    membres = [s.membre for s in souscriptions]

    return render(request, 'voir_membres_tontines.html', {
        'tontine': tontine,
        'membres': membres
    })





















'''
from django.shortcuts import render, redirect
from .models import pret
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def demande_pret(request):
    membres = membre.objects.exclude(user=request.user)  # exclure l'utilisateur lui-même

    if request.method == 'POST':
        montant = request.POST.get('montant')
        observations = request.POST.get('observations')
        cni_image = request.FILES.get('garant_cni_image')
        garant_id = request.POST.get('garant_id')

        membre_instance = membre.objects.get(user=request.user)

        if not cni_image or not garant_id:
            messages.error(request, "Veuillez sélectionner un garant et fournir la CNI.")
            return render(request, 'demande_pret.html', {'membres': membres})

        garant_instance = membre.objects.get(idmembre=garant_id)

        Pret = pret(
            montant=montant,
            observations=observations,
            garant_cni_image=cni_image,
            idmembre=membre_instance,
            garant=garant_instance
        )
        Pret.save()

        messages.success(request, "Votre demande de prêt a été soumise avec succès.")
        return redirect('liste_prets')

    return render(request, 'demande_pret.html', {'membres': membres})'''




from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import membre, pret
#
# @login_required
# def demande_pret(request):
#     membres = membre.objects.exclude(user=request.user)
#     tontine=Tontines.objects.all()
#
#     if request.method == 'POST':
#         montant = request.POST.get('montant')
#         observations = request.POST.get('observations')
#         cni_image = request.FILES.get('garant_cni_image')
#         garant_id = request.POST.get('garant_id')
#         tontine_id = request.POST.get('tontine_id')
#
#         membre_instance = membre.objects.get(user=request.user)
#
#         if not cni_image or not garant_id:
#             messages.error(request, "Veuillez sélectionner un garant et fournir la CNI.")
#             return render(request, 'demande_pret.html', {'membres': membres})
#
#         try:
#             garant_instance = membre.objects.get(idmembre=int(garant_id))
#             tontine_instance = Tontines.objets.get(idTontines=tontine_id)
#         except membre.DoesNotExist:
#             messages.error(request, "Le garant sélectionné est invalide.")
#             return render(request, 'demande_pret.html', {'membres': membres,'Tontines':tontine})
#
#         nouveau_pret = pret(
#             montant=montant,
#             idTontines=Tontines_instance,
#             observations=observations,
#             garant_cni_image=cni_image,
#             idmembre=membre_instance,
#             garant=garant_instance,
#             statut='en attente'
#         )
#         nouveau_pret.save()
#
#         messages.success(request, "Votre demande de prêt a été soumise avec succès.")
#         return redirect('liste_prets')

    # return render(request, 'demande_pret.html', {'membres': membres})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import membre, pret, Tontines  # IMPORTANT: Ajoute Tontines


@login_required
def demande_pret(request):
    # Récupère tous les membres sauf l'utilisateur connecté
    membres = membre.objects.exclude(user=request.user)

    # Récupère toutes les tontines
    tontines = Tontines.objects.all()

    if request.method == 'POST':
        montant = request.POST.get('montant')
        observations = request.POST.get('observations')
        cni_image = request.FILES.get('garant_cni_image')
        garant_id = request.POST.get('garant_id')
        tontine_id = request.POST.get('tontine_id')

        # Récupère le membre connecté
        membre_instance = membre.objects.get(user=request.user)

        # Validation
        if not cni_image or not garant_id:
            messages.error(request, "Veuillez sélectionner un garant et fournir la CNI.")
            return render(request, 'demande_pret.html', {
                'membres': membres,
                'tontines': tontines  # AJOUTER
            })

        try:
            garant_instance = membre.objects.get(idmembre=int(garant_id))
            tontine_instance = Tontines.objects.get(idTontines=int(tontine_id))
        except (membre.DoesNotExist, Tontines.DoesNotExist):
            messages.error(request, "Le garant ou la tontine sélectionné est invalide.")
            return render(request, 'demande_pret.html', {
                'membres': membres,
                'tontines': tontines  # AJOUTER
            })

        # Création du prêt
        nouveau_pret = pret(
            montant=montant,
            idTontines=tontine_instance,
            observations=observations,
            garant_cni_image=cni_image,
            idmembre=membre_instance,
            garant=garant_instance,
            statut='en attente'
        )
        nouveau_pret.save()

        messages.success(request, "Votre demande de prêt a été soumise avec succès.")
        return redirect('liste_prets')

    # CONTEXTE CORRIGÉ : Ajoute 'tontines' au dictionnaire
    return render(request, 'demande_pret.html', {
        'membres': membres,
        'tontines': tontines  # CE DICTIONNAIRE ÉTAIT MANQUANT !
    })

@login_required
def gestion_demandes(request):
    if request.user.membre.role != 'admin':
        return redirect('admin_dashboard')  # Redirige si ce n'est pas l'administrateur

    demandes = pret.objects.all()  # Récupérer toutes les demandes
    return render(request, 'gestion_demandes.html', {'demandes': demandes})





def liste_prets(request):
    prets = pret.objects.all()  # Récupérer tous les prêts
    return render(request, 'liste_prets.html', {'prets': prets})

@login_required






def valider_demande(request, idpret):
    # Vérifie que l'utilisateur est administrateur
    if not hasattr(request.user, 'membre') or request.user.membre.role != 'admin':
        return redirect('admin_dashboard')  # Redirige si ce n'est pas un admin

    # Récupère l'objet 'pret' via sa clé primaire personnalisée (idpret)
    demande = get_object_or_404(pret, idpret=idpret)

    # Met à jour le statut
    demande.statut = 'approuvé'
    demande.save()

    messages.success(request, "Demande de prêt approuvée avec succès.")
    return redirect('gestion_demandes')  # Remplace par la bonne vue



def refuser_demande(request, idpret):
    if request.user.membre.role != 'admin':
        return redirect('admin_dashboard')  # Redirige si ce n'est pas l'administrateur

    pret = get_object_or_404(pret, idpret=idpret)
    pret.statut = 'refusé'  # Mettre à jour le statut
    pret.save()
    messages.error(request, "Demande refusée.")
    return redirect('gestion_demandes')  # Redirige vers la page de gestion


from django.shortcuts import render
from .models import Souscription, pret  # Assurez-vous d'importer le modèle Pret



from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import pret, remboursement, Souscription

'''@login_required
def tableau_de_bord(request):
    membre = request.user.membre
    souscriptions = Souscription.objects.filter(membre=membre)
    prets = pret.objects.filter(idmembre=membre)

    prets_avec_remboursement = []

    for p in prets:
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant'))['total']

        if total_rembourse is None:
            total_rembourse = Decimal('0.00')
        
        reste = Decimal(p.montant) - total_rembourse
        if reste < 0:
            reste = Decimal('0.00')

        prets_avec_remboursement.append({
            'pret': p,
            'total_rembourse': total_rembourse.quantize(Decimal('0.01')),
            'reste': reste.quantize(Decimal('0.01'))
        })

    return render(request, 'tableau_de_bord.html', {
        'membre': membre,
        'souscriptions': souscriptions,
        'prets_avec_remboursement': prets_avec_remboursement
    })'''


from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Sum
from .models import Souscription, pret, remboursement, Don, membre

@login_required
def tableau_de_bord(request):
    membre_instance = request.user.membre
    souscriptions = Souscription.objects.filter(membre=membre_instance)
    prets = pret.objects.filter(idmembre=membre_instance)

    prets_avec_remboursement = []

    for p in prets:
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant'))['total']
        if total_rembourse is None:
            total_rembourse = Decimal('0.00')
        reste = Decimal(p.montant) - total_rembourse
        if reste < 0:
            reste = Decimal('0.00')

        prets_avec_remboursement.append({
            'pret': p,
            'total_rembourse': total_rembourse.quantize(Decimal('0.01')),
            'reste': reste.quantize(Decimal('0.01')),
            'garant_nom': p.garant.nom if p.garant else "Non défini",
            'garant_cni_url': p.garant_cni_image.url if p.garant_cni_image else None,
        })

    # Récupérer les dons du membre
    dons = Don.objects.filter(membre=membre_instance).order_by('-dateDon')

    total_dons_argent = dons.filter(typeDon='argent').aggregate(total=Sum('montant'))['total']
    if total_dons_argent is None:
        total_dons_argent = Decimal('0.00')

    return render(request, 'tableau_de_bord.html', {
        'membre': membre_instance,
        'souscriptions': souscriptions,
        'prets_avec_remboursement': prets_avec_remboursement,
        'dons': dons,
        'total_dons_argent': total_dons_argent.quantize(Decimal('0.01')),
    })





@login_required
def tableau_de_bord2(request):
    membre_instance = request.user.membre
    souscriptions = Souscription.objects.filter(membre=membre_instance)
    prets = pret.objects.filter(idmembre=membre_instance)

    prets_avec_remboursement = []

    for p in prets:
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant'))['total']
        if total_rembourse is None:
            total_rembourse = Decimal('0.00')
        reste = Decimal(p.montant) - total_rembourse
        if reste < 0:
            reste = Decimal('0.00')

        prets_avec_remboursement.append({
            'pret': p,
            'total_rembourse': total_rembourse.quantize(Decimal('0.01')),
            'reste': reste.quantize(Decimal('0.01')),
            'garant_nom': p.garant.nom if p.garant else "Non défini",
            'garant_cni_url': p.garant_cni_image.url if p.garant_cni_image else None,
        })

    # Récupérer les dons du membre
    dons = Don.objects.filter(membre=membre_instance).order_by('-dateDon')

    total_dons_argent = dons.filter(typeDon='argent').aggregate(total=Sum('montant'))['total']
    if total_dons_argent is None:
        total_dons_argent = Decimal('0.00')

    return render(request, 'tableau_de_bord2.html', {
        'membre': membre_instance,
        'souscriptions': souscriptions,
        'prets_avec_remboursement': prets_avec_remboursement,
        'dons': dons,
        'total_dons_argent': total_dons_argent.quantize(Decimal('0.01')),
    })









from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import pret, remboursement, membre
from django.utils import timezone
from django.contrib.auth.models import User

from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum

@login_required
def effectuer_remboursement(request):
    try:
        membre_connecte = membre.objects.get(user=request.user)
    except membre.DoesNotExist:
        messages.error(request, "Aucun profil membre associé à cet utilisateur.")
        return redirect('accueil')

    prets = pret.objects.filter(idmembre=membre_connecte)

    # Construction de la liste des prêts avec leur montant restant
    prets_avec_reste = []
    for p in prets:
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant'))['total']
        
        # Si aucun remboursement, le reste est le montant du prêt
        if total_rembourse is None:
            reste = Decimal(p.montant)
        else:
            total_rembourse = Decimal(total_rembourse)
            reste = Decimal(p.montant) - total_rembourse
            if reste < 0:
                reste = Decimal('0.00')

        prets_avec_reste.append({
            'pret': p,
            'reste': reste.quantize(Decimal('0.01'))  # Format propre avec 2 décimales
        })

    if request.method == "POST":
        idpret = request.POST.get('idpret')
        montant_rembourse = request.POST.get('montant')
        date_rembo = request.POST.get('dateRembo')

        if not all([idpret, montant_rembourse, date_rembo]):
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('effectuer_remboursement')

        try:
            pret_obj = pret.objects.get(idpret=idpret, idmembre=membre_connecte)
            try:
                montant_rembourse = Decimal(montant_rembourse)
            except InvalidOperation:
                messages.error(request, "Montant invalide.")
                return redirect('effectuer_remboursement')

            total_rembourse = remboursement.objects.filter(idpret=pret_obj).aggregate(total=Sum('montant'))['total']
            if total_rembourse is None:
                total_rembourse = Decimal('0.00')
            else:
                total_rembourse = Decimal(total_rembourse)

            reste = Decimal(pret_obj.montant) - total_rembourse

            if montant_rembourse > reste:
                messages.error(request, f"Le montant dépasse le reste à rembourser ({reste} F).")
                return redirect('effectuer_remboursement')

            remboursement.objects.create(
                idpret=pret_obj,
                montant=montant_rembourse,
                dateRembo=date_rembo
            )

            nouveau_reste = reste - montant_rembourse

            if nouveau_reste == 0:
                messages.success(request, "Remboursement complet effectué. Prêt soldé.")
            else:
                messages.warning(request, f"Remboursement partiel effectué. Montant restant : {nouveau_reste} F.")

        except pret.DoesNotExist:
            messages.error(request, "Prêt non trouvé.")

        return redirect('effectuer_remboursement')

    return render(request, 'effectuer_remboursement.html', {'prets_avec_reste': prets_avec_reste})






@login_required
def effectuer_remboursement2(request):
    try:
        membre_connecte = membre.objects.get(user=request.user)
    except membre.DoesNotExist:
        messages.error(request, "Aucun profil membre associé à cet utilisateur.")
        return redirect('accueil')

    prets = pret.objects.filter(idmembre=membre_connecte)

    # Construction de la liste des prêts avec leur montant restant
    prets_avec_reste = []
    for p in prets:
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant'))['total']
        
        # Si aucun remboursement, le reste est le montant du prêt
        if total_rembourse is None:
            reste = Decimal(p.montant)
        else:
            total_rembourse = Decimal(total_rembourse)
            reste = Decimal(p.montant) - total_rembourse
            if reste < 0:
                reste = Decimal('0.00')

        prets_avec_reste.append({
            'pret': p,
            'reste': reste.quantize(Decimal('0.01'))  # Format propre avec 2 décimales
        })

    if request.method == "POST":
        idpret = request.POST.get('idpret')
        montant_rembourse = request.POST.get('montant')
        date_rembo = request.POST.get('dateRembo')

        if not all([idpret, montant_rembourse, date_rembo]):
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('effectuer_remboursement2')

        try:
            pret_obj = pret.objects.get(idpret=idpret, idmembre=membre_connecte)
            try:
                montant_rembourse = Decimal(montant_rembourse)
            except InvalidOperation:
                messages.error(request, "Montant invalide.")
                return redirect('effectuer_remboursement2')

            total_rembourse = remboursement.objects.filter(idpret=pret_obj).aggregate(total=Sum('montant'))['total']
            if total_rembourse is None:
                total_rembourse = Decimal('0.00')
            else:
                total_rembourse = Decimal(total_rembourse)

            reste = Decimal(pret_obj.montant) - total_rembourse

            if montant_rembourse > reste:
                messages.error(request, f"Le montant dépasse le reste à rembourser ({reste} F).")
                return redirect('effectuer_remboursement2')

            remboursement.objects.create(
                idpret=pret_obj,
                montant=montant_rembourse,
                dateRembo=date_rembo
            )

            nouveau_reste = reste - montant_rembourse

            if nouveau_reste == 0:
                messages.success(request, "Remboursement complet effectué. Prêt soldé.")
            else:
                messages.warning(request, f"Remboursement partiel effectué. Montant restant : {nouveau_reste} F.")

        except pret.DoesNotExist:
            messages.error(request, "Prêt non trouvé.")

        return redirect('effectuer_remboursement')

    return render(request, 'effectuer_remboursement2.html', {'prets_avec_reste': prets_avec_reste})






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Don, membre

@login_required
def effectuer_don(request):
    try:
        membre = request.user.membre
    except membre.DoesNotExist:
        messages.error(request, "Profil membre introuvable.")
        return redirect('accueil')  # ou une autre page d’erreur

    if request.method == 'POST':
        type_don = request.POST.get('typeDon')
        montant = request.POST.get('montant') if type_don == 'argent' else None
        description = request.POST.get('description') if type_don == 'nature' else ''

        if type_don == 'argent' and not montant:
            messages.error(request, "Veuillez entrer un montant.")
        elif type_don == 'nature' and not description:
            messages.error(request, "Veuillez décrire le don en nature.")
        else:
            Don.objects.create(
                membre=membre,
                typeDon=type_don,
                montant=montant if montant else None,
                description=description
            )
            messages.success(request, 'Don enregistré avec succès.')
            return redirect('liste_dons_connecte')

    return render(request, 'effectuer_don.html', {'membre': membre})



@login_required
def liste_dons_connecte(request):
    try:
        membre = request.user.membre
    except membre.DoesNotExist:
        messages.error(request, "Profil membre introuvable.")
        return redirect('accueil')

    dons = Don.objects.filter(membre=membre)
    total = sum(d.montant for d in dons if d.typeDon == 'argent')
    return render(request, 'liste_dons_connecte.html', {
        'membre': membre,
        'dons': dons,
        'total': total
    })





from django.db.models import Sum

def liste_tous_les_dons(request):
    dons = Don.objects.all().order_by('-dateDon')
    total = Don.objects.filter(typeDon='argent').aggregate(Sum('montant'))['montant__sum'] or 0
    return render(request, 'liste_tous_les_dons.html', {
        'dons': dons,
        'total': total
    })






from django.shortcuts import render
from datetime import datetime
from .models import membre, Tontines
from django.db.models import Count

def statistiques_view(request):
    # Tranches d'âge
    current_year = datetime.now().year
    ages = [current_year - m.anneeNais for m in membre.objects.all() if m.anneeNais > 0]

    tranches = {
        '15-19': 0,
        '20-23': 0,
        '24-30': 0,
        '31-35': 0,
        '36+': 0,
    }

    for age in ages:
        if 15 <= age <= 19:
            tranches['15-19'] += 1
        elif 20 <= age <= 23:
            tranches['20-23'] += 1
        elif 24 <= age <= 30:
            tranches['24-30'] += 1
        elif 31 <= age <= 35:
            tranches['31-35'] += 1
        elif age > 35:
            tranches['36+'] += 1

    # Adhésion aux tontines
    tontines = Tontines.objects.all()
    tontine_data = {
    tontine.typeTontine: Souscription.objects.filter(tontine=tontine).count()
    for tontine in tontines
}

    context = {
        'tranche_labels': list(tranches.keys()),
        'tranche_data': list(tranches.values()),
        'tontine_labels': list(tontine_data.keys()),
        'tontine_data': list(tontine_data.values()),
    }

    return render(request, 'statistiques_view.html', context)



def statistiques_view2(request):
    # Tranches d'âge
    current_year = datetime.now().year
    ages = [current_year - m.anneeNais for m in membre.objects.all() if m.anneeNais > 0]

    tranches = {
        '15-19': 0,
        '20-23': 0,
        '24-30': 0,
        '31-35': 0,
        '36+': 0,
    }

    for age in ages:
        if 15 <= age <= 19:
            tranches['15-19'] += 1
        elif 20 <= age <= 23:
            tranches['20-23'] += 1
        elif 24 <= age <= 30:
            tranches['24-30'] += 1
        elif 31 <= age <= 35:
            tranches['31-35'] += 1
        elif age > 35:
            tranches['36+'] += 1

    # Adhésion aux tontines
    tontines = Tontines.objects.all()
    tontine_data = {
    tontine.typeTontine: Souscription.objects.filter(tontine=tontine).count()
    for tontine in tontines
}

    context = {
        'tranche_labels': list(tranches.keys()),
        'tranche_data': list(tranches.values()),
        'tontine_labels': list(tontine_data.keys()),
        'tontine_data': list(tontine_data.values()),
    }

    return render(request, 'statistiques_view2.html', context)
