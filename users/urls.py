from django.urls import path
from .views import selfcare_view,index_view,submit_assessment,contact_view,UserRegisterView, UserLoginView , logout_view, user_images,selfcare_view

urlpatterns = [
    path('', index_view, name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/images/', user_images, name='user_images'),
    
    path('contact/', contact_view, name='contact'),
    path('selfcare/', selfcare_view, name='selfcare'),

    path('submit-assessment/', submit_assessment, name='submit-assessment'),
]
