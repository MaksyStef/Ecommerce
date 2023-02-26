from django.views.generic import TemplateView


# Create your views here.
class SettingsView(TemplateView):
    template_name = 'account/settings.html'