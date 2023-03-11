from django import forms
from .models import Chaufferie

class nbChaudForm(forms.ModelForm):
  class Meta:
    model = Chaufferie
    fields = ["nbChaudiere"]
    labels = {'nbChaudiere': "Nombre Chaudière", "mobile_number": "Mobile Number",}