from django.shortcuts import render
import requests
from .forms import LoginForm
import json


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
    return render(request, 'applicant/userInfo.html')