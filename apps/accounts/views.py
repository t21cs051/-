from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from .forms import LoginForm

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from apps.accounts.forms import UserCreationForm

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'login.html'

class EmployeeAddView(View):
    form_class = UserCreationForm
    template_name = 'master/employee_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('master:employee')
        return render(request, self.template_name, {'form': form})
