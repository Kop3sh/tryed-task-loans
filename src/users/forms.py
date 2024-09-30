from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = models.EmailField(unique=True,blank=False,null=False)

    class Meta:
        model = User
        fields = ("email","first_name","last_name","is_staff",)
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class CustomUserChangeForm(UserChangeForm):
    pass