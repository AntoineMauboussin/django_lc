from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Identifiant :")
    password1 = forms.CharField(label="Mot de passe :")
    password2 = forms.CharField(label="Confirmation du mot de passe :")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Vous devez confrimer votre mot de passe")
        if password1 != password2:
            raise forms.ValidationError("Les mots de passe ne sont pas identiques")
        return password2