from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if not username or not password:
            raise forms.ValidationError("Please enter both fields")

        return super(LoginForm, self).clean()
