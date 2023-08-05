from django.forms import ModelForm
from .models import Set

class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = '__all__'