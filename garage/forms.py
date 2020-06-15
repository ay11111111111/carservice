from django import forms
from .models import Car


class CarCreationForm(forms.ModelForm):
    VOLUMES = ([(float("{0:.2f}".format(x*0.1)),float("{0:.2f}".format(x*0.1))) for x in range(11,65)])
    volume_dvigatel = forms.ChoiceField(choices=VOLUMES)
    class Meta:
        model = Car
        fields = ['car_model', 'year_of_issue','korobka', 'volume_dvigatel', 'probeg']
