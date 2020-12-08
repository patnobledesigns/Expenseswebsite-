from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
import json

from django.urls import reverse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
# Create your views here.


class EmailValidationView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, please choose another one'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use, please choose another one'}, status=409)
        return JsonResponse({'username_valid': True})


class RegisterationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/register.html')

    def post(self, request, *args, **kwargs):
        # Get User Data
        # Validate
        # Create a User Account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'account/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # Path_to_view
                # -getting domain we are on
                # -relative url to verification
                # -encode uid
                # - token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user)
                })
                activate_url = 'http://' + domain + link
                email_subject = 'Activate your account'
                email_body = f'Hi {user.username}, Please use this link to verify your account\n {activate_url}'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'account/register.html')

        return render(request, 'account/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message' + 'User already activated')
            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as e:
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, 'Welcome {}, You are now logged in.'.format(user.username))
                    return redirect('home')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'account/login.html')
            messages.error(
                request, 'Invalid credentials, try again.')
            return render(request, 'account/login.html')
        messages.error(
            request, 'Please fill all fields')
        return render(request, 'account/login.html')


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
            messages.success(request, 'You have been logged out.')
            return redirect('login')
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')
