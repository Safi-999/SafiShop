from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from .forms import RegistrationForm
from accounts.models import Account
from carts.views import _cart_id

import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte SVP !'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            #messages.success(
            #    request=request,
            #    message="Votre compte été crée avec succés ! Pour activer votre compte, consultez votre boite mail. "
            #)
            return redirect('/accounts/login/?command=verification&email='+email)
    else :
        form = RegistrationForm()

    context = {
            'form' : form,
        

    }
        
    return render(request, 'accounts/register.html', context)




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté')
            return redirect('dashboard')
        else:
            messages.error(request, 'Les informations entrées ne sont pas valides. Réessayez SVP !')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Vous êtes déconnecté ')
    return redirect('login')

    #return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitation ! Votre compte à été activé. Connectez vous maintenant')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):
    
    return render(request, 'accounts/dashboard.html')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password

            current_site = get_current_site(request=request)
            mail_subject = 'Réinitialisation de votre mot de passe'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email=email
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request, message="Nous venons de vous d'envoyer un e-mail. Consultez votre boite mail")
            return redirect('login')
        else:
            messages.error(request, message="Un compte n'existe pas avec cet adresse email") 
    return render(request, "accounts/forgotPassword.html")

        
    
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Réinitialisez votre mot passe SVP !')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Ce lien a expiré !')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Mot de passe modifié avec succès')
            return redirect('login')
        else:
            messages.error(request, 'Vous avez entrez différents mots de passe. Réessayez SVP !')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
