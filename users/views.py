from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse_lazy


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')