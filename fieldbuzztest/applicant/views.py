from django.shortcuts import render, redirect
import requests
from .forms import LoginForm, UserInfoForm
import json
import uuid
import time


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
            if response.status_code != 200:
                return render(request, 'applicant/login.html',  {'confirmation': 'Sign In failed. Try again !'})
            token = data['token']
            request.session['token'] = token
            return redirect('updateinfo')

    else:
        form = LoginForm()
    return render(request, 'applicant/login.html', {'form': form})


def userInfo(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            tsyncId = str(uuid.uuid4())
            cvTsyncId = str(uuid.uuid4())
            token = request.session.get('token')
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
            timeNow = int(time.time()*1000)
            pdf_file = request.FILES['uploadCv'].file.getvalue()
            file = {'file': pdf_file}

            ##Creating and uploading data to update userinfo
            applicantData = {'tsync_id': tsyncId, 'name': name, 'email': email, 'phone': phone, 'full_address': address, 'name_of_university': university,
                    'graduation_year': gradYear, 'cgpa': cgpa, 'experience_in_months':experience, 'current_work_place_name':currentWorkPlace,
                    'applying_in': appliedPosition, 'expected_salary': expectedSalary,'field_buzz_reference': reference, 'github_project_url':projectLink,
                    'cv_file': {'tsync_Id':cvTsyncId}, 'on_spot_creation_time': timeNow
                    }
            url = "https://recruitment.fisdev.com/api/v0/recruiting-entities/"
            headers = {'content-type': 'application/json', 'Authorization': f'Token {token}'}
            response = requests.post(url, data=json.dumps(applicantData), headers=headers)
            returnedData = response.json()
            print(returnedData)
            print(response.status_code)
            ## If response status is 'created' then retrive the cv_id,tsync_id and upload cv file.
            if response.status_code == 201:
                fileUploadUrl = f"https://recruitment.fisdev.com/api/file-object/{str(returnedData['cv_file']['id'])}/"
                file_headers = {'Authorization': f'Token {token}'}
                file_response = requests.patch(fileUploadUrl, files=file, headers=file_headers)
                if file_response.status_code == 200:
                    return render(request,'applicant/userInfo.html', {'confirmation': "Applican's info and CV uploaded successfully !"})
                else:
                    return render(request, 'applicant/userInfo.html', {'confirmation': "Couldn't upload CV"})
            else:
                return render(request, 'applicant/userInfo.html', {'confirmation': "Couldn't update information."})
    else:
        form = LoginForm()
    return render(request, 'applicant/userInfo.html', {'form': form})
