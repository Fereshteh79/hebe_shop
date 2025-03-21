import token
from audioop import reverse
from random import randint
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from ghasedakpack import ghasedakpack

from forms import LoginForm, RegisterForm, CheckOtpForm, OtpLoginForm, AddressCreationForm
from models import Otp
from testsms import sms

SMS = ghasedakpack.Ghasedak("")


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'invalid user data')
        else:
            form.add_error('phone', 'invalid data')
            return render(request, 'account/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/otp_login.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 999)
            SMS.verification(
                {'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode}
            )
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error("phone", "invalid data")

        return render(request, 'account/otp_login.html', {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'account/otp_login.html', {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 999)
            # SMS.verification(
            #     {'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'parm1': randcode}
            # )
            token = str(uuid4())
            Otp.objects.create(phone=cd['username'], code=randcode, token=token)
            return redirect(reverse('account:check_otp') + f'?token={str(token)}')
        else:
            form.add_error("phone", "invalide data")

        return render(request, 'account/otp_login.html', {'form': form})


def post(request):
    token = request.GET.get('token')
    form = CheckOtpForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if Otp.objects.filter(code=cd['code'], token=token).exists():
            otp = Otp.objects.get(token=token)
            user, is_create = User.objects.get_or_create(phone=otp.phone)
            login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
            otp.delete()
            return redirect('/')
    else:
        form.add_error("phone", "Invalid data")

    return render(request, 'account/check_otp.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})


def post(request):
    form = AddressCreationForm(request.POST)
    if form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        next_page = request.GET.get('next')
        if next_page:
            return redirect(next_page)
    return render(request, 'account/add_address.html', {'form': form})


class AddAddressView(View):

    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')
