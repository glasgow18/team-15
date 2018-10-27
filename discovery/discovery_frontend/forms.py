from django.forms import ModelForm

from discovery_frontend.models import Location


class AddLocationForm(ModelForm):

    class Meta:
        model = Location
        fields = '__all__'