from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from authapp.models import User
from adminapp.forms import UserAdminRegistrationForm, UserAdminProfileForim, ProductCategoryEditForm
from django.db import connection
from django.db.models import F, Q

# FBV  = Function-Based-Views
# CBC  = Class-Based-Views
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def index(request):
    context = {
        'title': 'GeekShop - Административная панель', }
    return render(request, 'index.html', context)


# READ
class UserListView(ListView):
    model = User
    template_name = 'admin-users-read.html'

    # queryset = User.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser,login_url='/')
# def admin_users(request):
#     context = {'users': User.objects.all()}
#     return render(request, 'admin-users-read.html', context)


# CREAT

class UserCreateView(CreateView):
    model = User
    template_name = 'admin-users-creat.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admin_staff:admin_users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser,login_url='/')
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#         else:
#             print(error)
#     else:
#         form = UserAdminRegistrationForm()
#     context = {
#         'title': 'GeekShop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'admin-users-creat.html', context)


# UPDATE
class UserUpdateView(UpdateView):
    model = User
    template_name = 'admin-users-update-delete.html'
    form_class = UserAdminProfileForim
    success_url = reverse_lazy('admin_staff:admin_users')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser,login_url='/')
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForim(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForim(instance=user)
#
#     context = {
#         'title': 'GeekShop - Профиль',
#         'form': form,
#         'user':user,
#     }
#
#     return render(request, 'admin-users-update-delete.html', context)


# DELETE

class UserDeleteView(DeleteView):
    model = User
    template_name = 'admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser,login_url='/')
# def admin_users_delete(request,user_id):
#     user = User.objects.get(id=user_id)
#     if user.is_active:
#         user.is_active = False
#     else:
#         user.is_active = True
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))


class ProductsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product_list.html'
    success_url = reverse_lazy('admin_staff:admin_users')


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'product-category-update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:index')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryUpdateView, self).dispatch(request, *args, **kwargs)