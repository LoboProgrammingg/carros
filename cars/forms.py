from django import forms
from cars.models import Car, CarReview
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'model', 
            'brand', 
            'factory_year', 
            'model_year', 
            'plate', 
            'value', 
            'photo', 
            'bio',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value < 20000:
            self.add_error('value', 'Valor mínimo do carro deve ser de R$20.000')
        return value

    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        if factory_year < 1975:
            self.add_error('factory_year', 'Não será possível cadastrar carros fabricados antes de 1975')
        return factory_year
    
    def save(self, commit=True):
        car = super().save(commit=False)
        if not car.user_id:
            if self.request:
                car.user = self.request.user
            else:
                raise ValueError('Request object not found. Cannot determine user.')
        if commit:
            car.save()
        return car
    
class StarRatingWidget(forms.RadioSelect):
    template_name = 'star_rating.html'

class CarReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=StarRatingWidget(attrs={'class': 'star-rating'}),
        label='Avaliação'
    )

    class Meta:
        model = CarReview
        fields = ['rating', 'comment']

class UserUpdateForm(UserChangeForm):
    username = forms.CharField(label='Nome de Usuário', max_length=150)

    class Meta:
        model = User
        fields = ('username',)

class UserCreationWithEmailForm(UserCreationForm):
    confirm_email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "confirm_email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email != confirm_email:
            raise forms.ValidationError("Os e-mails não correspondem.")
        return cleaned_data

class ProfileUpdateForm(forms.Form):
    old_password = forms.CharField(label='Senha Atual', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Nova Senha', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirme a Nova Senha', widget=forms.PasswordInput)

class FinanceCalculatorForm(forms.Form):
    price = forms.DecimalField(label='Preço do Carro', min_value=0)
    interest_rate = forms.DecimalField(label='Taxa de Juros (%)', min_value=0)
    loan_term = forms.IntegerField(label='Prazo do Financiamento (anos)', min_value=1)