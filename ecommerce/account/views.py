from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseGone
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account


# Create your views here.
class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'account/settings.html'


class SignView(TemplateView):
    template_name = "account/sign.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:settings')
        request.session['next_link'] = request.GET.get('next') 
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "login":
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            try:
                login(request, user)
                return redirect('store:homepage') if not request.session['next_link'] else redirect(request.session['next_link'])
            except:
                request.session['login_error'] = "Invalid credentials."
                return self.get(request, *args, **kwargs)
        if request.POST.get('action') == "register":
            if request.POST.get('password') != request.POST.get('confirmation'):
                request.session['register_error'] = "Your password and confirmation do not match"
                return self.get(request, *args, **kwargs)
            try:
                user = Account.objects.create_user(
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    first_name=request.POST.get('firstName'),
                    last_name=request.POST.get('secondName'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    postal_code=request.POST.get('postalCode'),
                    password=request.POST.get('password'),
                )
            except Exception as e:
                e = str(e)
                if "username" in e:
                    request.session['register_error'] = "The username is already taken. Please choose a different one."
                if "email" in e:
                    request.session['register_error'] = "The email is already taken. Please choose a different one."
                return self.get(request, *args, **kwargs)
            login(request, user)
            return redirect('store:homepage') if not request.session['next_link'] else redirect(request.session['next_link'])
        return HttpResponseBadRequest(content="Action is not allowed or missing")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context.update({
            "login_error": request.session.get('login_error') if request.session.get('login_error') else None,
            "register_error": request.session.get('register_error') if request.session.get('register_error') else None,
        })
        return context
    
        
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('store:homepage')