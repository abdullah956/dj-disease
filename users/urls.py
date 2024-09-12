from django.urls import path
from .views import index_view ,  UserRegisterView, UserLoginView , logout_view

urlpatterns = [
    path('', index_view, name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
