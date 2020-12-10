from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from rest_framework.exceptions import ValidationError


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
    github_validator = RegexValidator(r"github.com/", "Provide a valid github link.")
    name = forms.CharField(max_length=256,required=True)
    email = forms.EmailField(max_length=256)
    phone = forms.CharField(max_length=14)
    address = forms.CharField(max_length=512,required=False)
    university = forms.CharField(max_length=256)
    gradYear = forms.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2020)])
    cgpa = forms.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(4.0)], required=False)
    experience = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],required=False)
    currentWorkPlace = forms.CharField(max_length=256,required=False)
    appliedPosition = forms.ChoiceField(choices=Position_Choices)
    expectedSalary = forms.IntegerField(validators=[MinValueValidator(15000), MaxValueValidator(60000)])
    reference = forms.CharField(max_length=256,required=False)
    projectLink = forms.CharField(max_length=512,validators=[github_validator])
    uploadCv = forms.FileField(validators=[FileExtensionValidator(['pdf'])])

    def clean_cv(self):
        cvFile = self.cleaned_data.get('uploadCv')
        if cvFile:
            if cvFile.size > 4194304:
                raise ValidationError("File size exceeds 4MB.")
            return cvFile
        else:
            raise ValidationError("Upload failed.")


