from django.contrib.auth.forms import UserCreationForm
from .models import CustomUsers

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUsers
        fields = ['username', 'email', 'phone', 'password1', 'password2']