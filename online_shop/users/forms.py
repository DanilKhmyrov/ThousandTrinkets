from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegistrationUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
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
        return user
