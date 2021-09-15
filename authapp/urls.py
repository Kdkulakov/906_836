from django.urls import path

# from authapp.views import login, register, profile, new_logout
from authapp.views import LoginListView, RegisterListView, ProfileFormView, new_logout,RegisterListView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('new-logout/', new_logout, name='new_logout'),
    path('verify/<str:email>/<str:activation_key>/', RegisterListView.verify, name='verify'),

]
