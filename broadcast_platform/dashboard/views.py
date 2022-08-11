from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/home.html'
    context_object_name = 'users'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user is not None:
                return render(request, self.template_name)
        else:
            return redirect('login')

def error400(request, exception=None):
    template_name = 'dashboard/400.html'
    return render(request, template_name)


def error403(request, exception=None):
    template_name = 'dashboard/403.html'
    return render(request, template_name)


def error404(request, exception=None):
    template_name = 'dashboard/404.html'
    return render(request, template_name)


def error500(request, exception=None):
    template_name = 'dashboard/500.html'
    return render(request, template_name)
