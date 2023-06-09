from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username:")
    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation:", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You need to confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class ShareForm(forms.Form):
    username = forms.CharField(label="Username you want to share with:")
            
