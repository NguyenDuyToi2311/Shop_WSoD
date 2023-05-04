from django import forms
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import *

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # username = forms.CharField(label="User Name", required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        label = {"email", "Email"}
        widgets = {"username": forms.TextInput(attrs={"class": "form-control"})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
            }
        ),
        help_text=_("Enter your password"),
    )


class PasswordChangeForm(PasswordChangeForm):
    # strip là loại bỏ khoảng trắng đầu và cuối, mặc định là True
    # widget hiển thị trường cho người dùng, ở đây dùng passwordinput thì hiện tra trường ẩn password
    # attrs(attribute) được áp dụng cho widget của trường đó trên giao diện người dùng
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
            }
        ),
        help_text=_("Enter your password"),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                # "autocomplete": "new-password" chỉ định rằng đây là một trường mật khẩu mới và
                # trình duyệt không nên đề xuất lại các giá trị nhập trước đó
                "class": "form-control",
            }
        ),
        help_text=_("Enter your new password"),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
        help_text=_("Enter your new password"),
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=256,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}),
    )


class PasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
    )
    
class CustomerProfileForm(forms.ModelForm):   
    class Meta:
        model = Customer
        fields= ['name', 'address', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'})
        }









