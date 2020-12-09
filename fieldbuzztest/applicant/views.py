from django.shortcuts import render
import requests
from .forms import LoginForm, UserInfoForm
import json
import uuid


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            url = 'https://recruitment.fisdev.com/api/login/'
            data = {'username': username, 'password': password}
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            data = response.json()
            token = data['token']
            if response.status_code != 200:
                return render(request, 'applicant/login.html', {'serverError': "Couldn't Sign In properly"})
            return render(request, 'applicant/userinfo.html', {'token': token})

    else:
        form = LoginForm()
    return render(request, 'applicant/login.html', {'form': form})


def userInfo(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            tsyncId = str(uuid.uuid4())
            cvTsyncId = str(uuid.uuid4())
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            university = form.cleaned_data['university']
            gradYear = form.cleaned_data['gradYear']
            cgpa = form.cleaned_data['cgpa']
            experience = form.cleaned_data['experience']
            currentWorkPlace = form.cleaned_data['currentWorkPlace']
            appliedPosition = form.cleaned_data['appliedPosition']
            expectedSalary = form.cleaned_data['expectedSalary']
            reference = form.cleaned_data['reference']
            projectLink = form.cleaned_data['projectLink']
            print(tsyncId)
            print(cvTsyncId)
            cv = {'tsync_id': cvTsyncId}
            ##cv_file = json.dumps((cv))
            data = {'tsync_id': tsyncId,'name': name, 'email': email, 'phone': phone, 'full_address': address, 'name_of_university':university,
                    'graduation_year': gradYear,'cgpa': cgpa, 'experience_in_months':experience,
                    'current_work_place_name':currentWorkPlace, 'applying_in': appliedPosition, 'expected_salary': expectedSalary,
                    'field_buzz_reference': reference, 'github_project_url':projectLink, 'cv_file': {'tsync_Id':cvTsyncId}
                    }
            print(json.dumps(data))
            return render(request, 'applicant/userInfo.html', {'confirmation': 'Succeded'})

    else:
        form = LoginForm()
    return render(request, 'applicant/userInfo.html', {'form':form})
