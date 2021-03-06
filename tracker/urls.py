from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('register_user', views.register_user),
    path('login', views.login_user),
    path('dashboard', views.user_home),
    path('logout', views.logout),
    path('create', views.new_project),
    path('project/<int:projID>', views.view_project),
]
