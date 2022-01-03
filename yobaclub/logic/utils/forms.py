from django import forms

class SignUpForm(forms.Form):
    login = forms.CharField(label="User's login", max_length=25, required=True, min_length=3)
    mail = forms.EmailField(label="User's email", required=True)
    password = forms.CharField(label="User's password", required=True, max_length=200, min_length=8)
    password_confirm = forms.CharField(label="User's password second time", required=True, max_length=200, min_length=8)

    def is_valid(self) -> bool:
        return super().is_valid() and self.cleaned_data.get('password') == self.cleaned_data.get('password_confirm')