from django.contrib import admin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserModelAdmin(UserAdmin):
    add_form = CustomUserCreationForm  
    form = CustomUserChangeForm  
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
        "birth_date",
        "username",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    )
    fieldsets = (
        ("General", {"fields": ("email",
                                "phone_number",
                                "first_name",
                                "last_name",
                                "birth_date",
                                "height",
                                "weight",
                                "gender",
                                "lang",
                                "payments_id",
                                "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    search_fields = ("email","id")
    ordering = ("date_joined",)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','password1', 'password2', 'is_staff', )}
        ),
    )
    def clean(self):
        super(UserModelAdmin, self).clean()

admin.site.register(User, UserModelAdmin)