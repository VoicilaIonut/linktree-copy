from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from .forms import  NewUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login
from django.http import HttpResponse

class SignUpView(View):
    form_class = NewUserForm
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            if not form.cleaned_data['username'].islower() or not form.cleaned_data['username'].isalpha():
                form.add_error('username', 'Invalid username')
                return render(request, self.template_name, {'form': form})

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('user/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponse('Please confirm your e-mail to complete the registration.')

        if form.has_error('username'):
            form.errors['username'] = ['Invalid username']

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponse('Thank you for the confirmation by email.')
        else:
        	return HttpResponse('The confirmation link was invalid, probably because it was already in use.')