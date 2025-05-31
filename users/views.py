from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from .forms import UserLoginForm, UserRegisterForm
from .models import User


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request=self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect("products:main_page")
        else:
            return self.form_invalid(form)


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user.username = email
        user.save()
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect("products:main_page")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("products:main_page")


@method_decorator(
    login_required(login_url="/user/login", redirect_field_name=None), name="dispatch"
)
class UserProfileView(TemplateView):
    template_name = "users/user_profile.html"
