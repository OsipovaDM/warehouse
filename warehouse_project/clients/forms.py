from django import forms

from storage.models import Clients


class ClientsForm(forms.ModelForm):

    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'description': forms.Textarea({'cols': '22', 'rows': '5'}),
            'comment': forms.Textarea({'cols': '22', 'rows': '5'}),
        }
