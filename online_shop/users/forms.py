from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from store.models import ShoppingCart

User = get_user_model()


class RegistrationUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = 'Необязательное поле'
        self.fields['phone_number'].help_text = 'Необязательное поле'
        self.fields['phone_number'].label = 'Введите ваш номер телефона'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            ShoppingCart.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control custom-input', 'type': 'date'}),
        label='День рождения',
        input_formats=['%d-%m-%Y'],
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'birthdate', 'phone_number',)
        help_texts = {
            'username': 'Имя пользователя должно быть уникальным.',
            'first_name': 'пися.',
            'last_name': 'попа.',
            'phone_number': '123'
        }
