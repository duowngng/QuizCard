from django.forms import ModelForm
from .models import Set, Card

class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = '__all__'
        exclude = ['user']
        
class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ['set']