from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='docshare/registration/login.html', next_page='/'), name='login'),
	path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
]
