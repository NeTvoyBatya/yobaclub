from django import forms
from yobaclub.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth import authenticate, login


class SignUpForm(forms.Form):
    login = forms.CharField(label="User's login", max_length=25, required=True, min_length=3)
    mail = forms.EmailField(label="User's email", required=True)
    password = forms.CharField(label="User's password", required=True, max_length=200, min_length=8)
    password_confirm = forms.CharField(label="User's password second time", required=True, max_length=200, min_length=8)

    def is_valid(self) -> bool:
        return super().is_valid() and self.cleaned_data.get('password') == self.cleaned_data.get('password_confirm')

    def save_user(self) -> bool:
        try:
            hasher = PBKDF2PasswordHasher()
            login = self.cleaned_data.get("login")
            password = self.cleaned_data.get("password")
            password = hasher.encode(password, hasher.salt())
            email = self.cleaned_data.get("mail")
            user = User(login, password, email)
            user.save()
            return True
        except Exception as e:
            print(e.__repr__())
            return False

class SignInForm(forms.Form):
    login = forms.CharField(label="User's login or email", required=True, min_length=3)
    password = forms.CharField(label="User's password", required=True, max_length=200, min_length=8)
    remember = forms.BooleanField(required=False)

    def process_login(self) -> None:
        if "@" in self.cleaned_data.get("login"):
            self.login_type = "mail"
        else:
            self.login_type = "login"
    
    def login_user(self, request) -> bool:
        data = self.cleaned_data
        user = authenticate(request, login=data.get("login"), login_type=self.login_type, password=data.get("password"))
        if user is not None and request.user.is_anonymous:
            login(request, user)
            if not data.get("remember"):
                request.session.set_expiry(0)
            return True
        return False    

    def is_valid(self) -> bool:
        valid = super().is_valid()
        self.process_login()
        return valid