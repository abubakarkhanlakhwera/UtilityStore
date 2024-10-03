from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.auth_page, name='auth_page'),  # Show login/signup page if not authenticated
    path('signup/', views.signup, name='signup'),  # Sign up page
    path('login/', auth_views.LoginView.as_view(template_name='authapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
