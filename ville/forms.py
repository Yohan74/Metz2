from django import forms

from .models import SELECTION

# SELECTION = (
#     ('Quartier', 'Quartier'),
#     ('Eglise', 'Eglise'),
#     ('Cathédrale', 'Cathédrale'),
# )

class Upload_Form(forms.Form):
    selection = forms.ChoiceField(
            widget=forms.RadioSelect, choices=SELECTION, label="")
    verification = forms.BooleanField(required=False, label="A verifier ? ")


