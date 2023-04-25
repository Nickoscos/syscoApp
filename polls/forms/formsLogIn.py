from django import forms

#Formulaire de connexion
class loginForm(forms.ModelForm):
  class Meta:
    fields = ["username", "password"]
    labels = {'username': "Nom d'utilisateur", 'password': "Mot de passe"}