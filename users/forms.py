from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Эти поля НЕ будут сохранены в User, только в UserProfile
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Убрал phone и address

    # Добавляем метод для сохранения в UserProfile
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаём профиль с телефоном и адресом
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']