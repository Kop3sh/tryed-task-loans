from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = models.EmailField(unique=True,blank=False,null=False)

    class Meta:
        model = User
        fields = ("email","is_staff",)
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class CustomUserChangeForm(UserChangeForm):
    pass