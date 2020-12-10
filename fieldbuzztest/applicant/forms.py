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
    full_address = forms.CharField(max_length=512,required=False)
    name_of_university = forms.CharField(max_length=256)
    graduation_year = forms.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2020)])
    cgpa = forms.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(4.0)], required=False)
    experience_in_months = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],required=False)
    current_work_place_name = forms.CharField(max_length=256,required=False)
    applying_in = forms.ChoiceField(choices=Position_Choices)
    expected_salary = forms.IntegerField(validators=[MinValueValidator(15000), MaxValueValidator(60000)])
    field_buzz_reference = forms.CharField(max_length=256,required=False)
    github_project_url = forms.CharField(max_length=512,validators=[github_validator])
    uploadCv = forms.FileField(validators=[FileExtensionValidator(['pdf'])])

    def clean_cv(self):
        cvFile = self.cleaned_data.get('uploadCv')
        if cvFile:
            if cvFile.size > 4194304:
                raise ValidationError("File size exceeds 4MB.")
            return cvFile
        else:
            raise ValidationError("Upload failed.")


