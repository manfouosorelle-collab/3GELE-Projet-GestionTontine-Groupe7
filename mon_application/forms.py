from django import forms
from .models import *


class connexionForm(forms.Form):
    
        email = forms.CharField(widget=forms.EmailInput)
        password = forms.CharField(widget=forms.PasswordInput)
        nom = forms.CharField(widget=forms.EmailInput)


class membreForm(forms.ModelForm):
    class Meta:
        model = membre
        fields = ['password', 'email','nom', 'prenom', 'anneeEntree', 'anneeNais','telephone','actif', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }


class TontineForm(forms.ModelForm):
    class Meta:
        model = Tontines
        fields = ['typeTontine', 'montant']


class RemboursementForm(forms.ModelForm):
    class Meta:
        model = remboursement
        fields = ['dateRembo', 'montant']
        widgets = {
            'dateRembo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montantRembo': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class AjouterMembreTontineForm(forms.Form):
    membre = forms.ModelChoiceField(queryset=membre.objects.all())
    tontine = forms.ModelChoiceField(queryset=Tontines.objects.all())