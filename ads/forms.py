from django import forms
from .models import Ad, ExchangeProposal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition', 'price']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'price': 'Цена',
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
            'condition': 'Состояние',
            
        }
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        labels = {
            'ad_sender': 'Ваше объявление',
            'ad_receiver': 'Объявление для обмена',
            'comment': 'Комментарий'
        }
