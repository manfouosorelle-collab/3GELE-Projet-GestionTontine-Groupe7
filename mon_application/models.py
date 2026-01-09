from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone







class membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idmembre = models.AutoField(db_column='idmembre', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='nom', max_length=30)  # Field name made lowercase.
    prenom = models.CharField(db_column='prenom', max_length=30)  # Field name made lowercase.
    anneeNais = models.IntegerField(db_column='anneeNais', default=0)  # Field name made lowercase.
    anneeEntree = models.IntegerField(db_column='anneeEntree', default=0)  # Field name made lowercase.
    password = models.CharField(db_column='password', max_length=1000)  # Field name made lowercase.
    telephone = models.CharField(db_column='telephone',  max_length=15)
    email = models.CharField(db_column='email',  max_length=50)
    actif = models.IntegerField(db_column='actif', default=1)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('membre', 'Membre')])
    
    def __str__(self):
        return self.nom
   




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username    

    class Meta:
        db_table = 'membre'


class Tontines(models.Model):
    TYPE_CHOICES = [
        ('presence', 'Tontine de Présence'),
        ('epargne', 'Tontine d_epargne'),
        ('solidarite', 'Tontine de solidarite'),
        ('rotative', 'Tontine rotative'),
    ]
    
    idTontines = models.AutoField(db_column='idTontines', primary_key=True) 
    typeTontine = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.typeTontine} : {self.montant} F"
    
    class Meta:
        db_table = 'Tontines'


class Souscription(models.Model):
    tontine = models.ForeignKey(Tontines, on_delete=models.CASCADE)
    membre = models.ForeignKey(membre, on_delete=models.CASCADE)
    date_souscription = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Souscription de {self.membre.nom} à {self.tontine.typeTontine}"





class epargne(models.Model):
    idEpargne = models.AutoField(db_column='idEpargne', primary_key=True)  # Field name made lowercase.
    montant = models.DecimalField(db_column='montant',  max_digits=19, decimal_places=4)  # Field name made lowercase.
    modeVersement = models.CharField(db_column='modeVersement', max_length=20)  # Field name made lowercase.
    couponVersement = models.CharField(db_column='couponVersement', max_length=64)  # Field name made lowercase.
    idmembre = models.ForeignKey(membre, on_delete=models.CASCADE, db_column='idmembre')
    dateseance = models.DateField(db_column='dateseance')  # Field name made lowercase.
    

    class Meta:
        db_table = 'epargne'


class pret(models.Model):
    idpret = models.AutoField(db_column='idpret', primary_key=True)
    datepret = models.DateTimeField(auto_now_add=True)
    tauxInteret = models.DecimalField(max_digits=15, decimal_places=2, default=5.0)
    montant = models.DecimalField(db_column='montant', max_digits=15, decimal_places=2)
    observations = models.TextField(db_column='observations', blank=True, null=True)
    idmembre = models.ForeignKey(membre, on_delete=models.CASCADE, db_column='idmembre')
    dateseance = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='en attente')
    garant = models.ForeignKey(membre, on_delete=models.CASCADE, related_name='garant_de', null=True)
    garant_cni_image = models.ImageField(upload_to='cni_garants/', blank=False, null=True)
    idTontines = models.ForeignKey(Tontines, on_delete=models.CASCADE, db_column='idTontines')

    class Meta:
        db_table = 'pret'
# class pret(models.Model):
#     idpret = models.AutoField(db_column='idpret', primary_key=True)  # Field name made lowercase.
#     datepret = models.DateTimeField(auto_now_add=True)
#     tauxInteret = models.DecimalField(max_digits=15, decimal_places=2, default=5.0)
#     montant = models.DecimalField(db_column='montant', max_digits=15, decimal_places=2)  # Field name made lowercase.
#     observations = models.TextField(db_column='observations', blank=True, null=True)  # Field name made lowercase.
#     idmembre = models.ForeignKey(membre, on_delete=models.CASCADE, db_column='idmembre')
#     dateseance = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
#     statut = models.CharField(max_length=20, default='en attente')  # 'en attente',
#     garant = models.ForeignKey(membre, on_delete=models.CASCADE, related_name='garant_de', null=True)
#
#     garant_cni_image = models.ImageField(upload_to='cni_garants/', blank=False, null=True)
#
#     idTontines = models.ForeignKey(Tontines, on_delete=models.CASCADE, db_column='idTontines')
#     dateseance = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
#     statut = models.CharField(max_length=20, default='en attente')  # 'en attente',
#     garant= models.ForeignKey(Tontines, on_delete=models.CASCADE, related_name='garant_de', null=True)
#
#     class Meta:
#         db_table = 'pret'


class remboursement(models.Model):
    idRembo = models.AutoField(db_column='idRembo', primary_key=True)  # Field name made lowercase.
    dateRembo= models. DateField(db_column='dateRembo')
    montant = models.DecimalField(db_column='montant', max_digits=15, decimal_places=2)  # Field name made lowercase.
    idpret = models.ForeignKey(pret, on_delete=models.CASCADE,db_column='idpret')
    dateseance = models.DateField(auto_now_add=True)  # Field name made lowercase.
    

    class Meta:
        db_table = 'remboursement'

    def __str__(self):
        return f'Remboursement de {self.montant} F pour le prêt {self.idpret}'

class sanction(models.Model):
    idSanction = models.AutoField(db_column='idTontines', primary_key=True)  # Field name made lowercase.
    dateSanction = models.DateField(db_column='dateSanction')  # Field name made lowercase.
    typeSanction = models.CharField(db_column='typeTontine', max_length=50)  # Field name made lowercase.
    montant = models.DecimalField(db_column='montantTontine', max_digits=15, decimal_places=2)  # Field name made lowercase.
    idmembre = models.ForeignKey(membre, on_delete=models.CASCADE, db_column='idmembre')  # Field name made lowercase.
    raison = models.TextField(db_column='raison', blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        db_table = 'sanction'



'''class versementTontine(models.Model):
    idVersTontine = models.AutoField(db_column='idVersCotis', primary_key=True)  # Field name made lowercase.
    montant = models.DecimalField(db_column='montant',max_digits=15, decimal_places=2 )  # Field name made lowercase.
    modeVersement = models.CharField(db_column='modeVersement', max_length=20)  # Field name made lowercase.
    couponVersement = models.CharField(db_column='copuonVersement',max_length= 64 )  # Field name made lowercase.
    idmembre = models.ForeignKey(membre, on_delete=models.CASCADE ,db_column='idmembre')
    idTontines = models.ForeignKey(Tontines, on_delete=models.CASCADE,db_column='codeCotisation')
    dateseance = models.DateField(db_column='idSeance')  # Field name made lowercase.

    class Meta:
        db_table = 'versementTontine'

'''

class Don(models.Model):
    TYPE_CHOICES = (
        ('argent', 'Don en argent'),
        ('nature', 'Don en nature'),
    )

    idDon = models.AutoField(primary_key=True)
    dateDon = models.DateField(default=timezone.now)
    typeDon = models.CharField(max_length=10, choices=TYPE_CHOICES, default='argent')
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)  # Pour les dons en nature
    membre = models.ForeignKey(membre, on_delete=models.CASCADE)

    def __str__(self):
        if self.typeDon == 'argent':
            return f"{self.membre.nom} - {self.montant}F"
        else:
            return f"{self.membre.nom} - Don en nature : {self.description}"






   

# Create your models here.
