from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from authapp.forms import UserRegisterForm, UserLoginForm, UserProfileForm
from django.contrib import messages
from authapp.models import User
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView

# FBV  = Function-Based-Views
# CBC  = Class-Based-Views
from geekshop import settings


class LoginListView(LoginView):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context

    # def get_queryset(self,**kwargs):
    #    return f


# # функцияя = вьюхи = контролеры.
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'GeekShop - Авторизация',
#         'form': form,
#     }
#     return render(request, 'authapp/login.html', context)

class RegisterListView(FormView):
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    # success_message = 'Вы успешно зарегистрировались!'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(RegisterListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect(self.success_url)

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def send_verify_mail(self, user):
        verify_link = reverse_lazy('authapp:verify', args=[user.email, user.activation_key])

        title = f'Для активации учетной записи {user.username} пройдите по ссылке'

        messages = f'Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}' \
                   f'{verify_link}'

        return send_mail(title, messages, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expires():
                user.is_active = True
                user.save()
                auth.login(self, user)
                return render(self, 'mainapp/index.html')
            else:
                print(f'error activation user: {user}')
                return render(self, 'authapp/verification.html')
        except Exception as e:
            print(f'error activation user : {e.args}')
            return HttpResponseRedirect(reverse('index'))

    # def form_valid(self, form):
    #     form.save()
    #     username = self.request.POST['username']
    #     password = self.request.POST['password1']
    #     user = authenticate(username=username,password=password)
    #     login(self.request,user)
    #     return super(RegisterListView, self).form_valid(form)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'GeekShop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'authapp/register.html', context)


def new_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class ProfileFormView(FormView):
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('auth:profile')

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Профиль'
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileFormView, self).dispatch(request, *args, **kwargs)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {
#         'form': form,
#         'title': 'GeekShop - Профиль',
#         'baskets': Basket.objects.filter(user=request.user), }
#     return render(request, 'authapp/profile.html', context)
