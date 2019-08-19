from django import forms
from .models import Menu, Option, Order
from django.contrib.auth.models import User

class OptionForm(forms.ModelForm):
    """
    A class used to make a option form
    """
    class Meta:
        model = Option
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la opción, Ej: Arroz con pollo'
            })
        }


class MenuForm(forms.ModelForm):
    """
    A class used to make a menu form
    """
    class Meta:
        model = Menu
        fields = ('date', 'options')
        widgets = {
            'options': forms.SelectMultiple(
                attrs={'class': 'select2'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%d/%m/%Y', ]
        self.fields['date'].widget = forms.DateInput(
            format='%d/%m/%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'Ingrese la fecha del menu'})


class OrderForm(forms.ModelForm):
    """
    A class used to make a order form
    """
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            options_choice = Menu.objects.filter(pk=kwargs['initial']['menu'].id)[0].options.all()
        else:
            options_choice = Option.objects.all()

        self.fields['menu'] = forms.ModelChoiceField(queryset=Menu.objects.all(), widget=forms.Select(attrs={'class': 'select2'}))
        self.fields['option'] = forms.ModelChoiceField(queryset=options_choice, widget=forms.Select(attrs={'class': 'select2'}))
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'select2'}))
        self.fields['customizations'].widget = forms.Textarea(attrs={
            'class': 'form-control'
        })

    class Meta:
        model = Order
        fields = ('menu', 'user', 'option', 'customizations')