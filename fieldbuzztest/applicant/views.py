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
                return render(request, 'applicant/login.html', {'confirmation': 'Sign In failed. Try again !'})
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
            post_data = request.POST.dict()
            sorted_data = {key: value for key, value in post_data.items() if
                           value != '' and key != 'csrfmiddlewaretoken'}
            f_data = {key: value for key, value in sorted_data.items() if value.isspace() != True}

            token = request.session.get('token')
            tsyncId = str(uuid.uuid4())
            cvTsyncId = str(uuid.uuid4())
            timeNow = int(time.time() * 1000)
            pdf_file = request.FILES['uploadCv'].file.getvalue()
            file = {'file': pdf_file}

            applicantData = {'tsync_id': tsyncId, 'cv_file': {'tsync_Id': cvTsyncId}, 'on_spot_creation_time': timeNow}
            applicantData.update(f_data)
            url = "https://recruitment.fisdev.com/api/v1/recruiting-entities/"
            headers = {'content-type': 'application/json', 'Authorization': f'Token {token}'}
            response = requests.post(url, data=json.dumps(applicantData), headers=headers)
            returnedData = response.json()

            if response.status_code == 201:
                fileUploadUrl = f"https://recruitment.fisdev.com/api/file-object/{str(returnedData['cv_file']['id'])}/"
                file_headers = {'Authorization': f'Token {token}'}
                file_response = requests.put(fileUploadUrl, files=file, headers=file_headers)
                if file_response.status_code == 200:
                    return render(request, 'applicant/userInfo.html',
                                  {'confirmation': "Applicant's info and CV uploaded successfully !"})
                else:
                    return render(request, 'applicant/userInfo.html', {'confirmation': "Couldn't upload CV"})
            else:
                return render(request, 'applicant/userInfo.html', {'confirmation': "Couldn't update information."})
    else:
        form = LoginForm()
    return render(request, 'applicant/userInfo.html', {'form': form})
