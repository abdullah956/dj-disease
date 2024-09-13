from django.urls import path
from .views import index_view ,info_view,triggers_view, symptoms_view,avoid_view,about_view, emergency_view,UserRegisterView, UserLoginView , logout_view, user_images,selfcare_view

urlpatterns = [
    path('', index_view, name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/images/', user_images, name='user_images'),

    
    path('about/', about_view, name='about'),
    path('emergency/', emergency_view, name='emergency'),
    path('avoid/', avoid_view, name='avoid'),
    path('info/', info_view, name='info'),
    path('selfcare/', selfcare_view, name='selfcare'),
    path('symptoms/', symptoms_view, name='symptoms'),
    path('triggers/', triggers_view, name='triggers'),
]
