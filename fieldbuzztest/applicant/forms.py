from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError('Enter your username please !')
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Enter Your password please")
        return password


class UserInfoForm(forms.Form):
    Position_Choices = (
        ("Mobile", "Mobile"),
        ("Backend", "Backend"),
    )
    name = forms.CharField(max_length=256,required=True)
    email = forms.EmailField(max_length=256)
    phone = forms.CharField(max_length=14)
    address = forms.CharField(max_length=512,required=False)
    university = forms.CharField(max_length=256)
    gradYear = forms.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2020)])
    cgpa = forms.FloatField(required=False)
    experience = forms.IntegerField(required=False)
    currentWorkPlace = forms.CharField(max_length=256,required=False)
    appliedPosition = forms.ChoiceField(choices=Position_Choices)
    expectedSalary = forms.IntegerField()
    reference = forms.CharField(max_length=256,required=False)
    projectLink = forms.CharField(max_length=512)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError('Enter your username please !')
        return name
