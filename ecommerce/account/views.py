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
    next_link:str = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:settings')
        self.next_link = request.GET.get('next') 
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "login":
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            login(request, user)
            return redirect('store:homepage') if not self.next_link else redirect(self.next_link)
        if request.POST.get('action') == "register":
            if request.POST.get('password') != request.POST.get('confirmation'):
                return JsonResponse({'err_message': "Your password and confirmation do not match"})
            user = Account.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
            login(request, user)
            return redirect('store:homepage') if not self.next_link else redirect(self.next_link)
        return HttpResponseBadRequest(content="Action is not allowed or missing")
        
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('store:homepage')