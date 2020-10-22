from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('welcome', views.dashboard),
    path('logout', views.logout),
    path('addJob', views.add_job),
    path('add', views.add),
    path('view/<int:id>', views.view),
    path('edit/<int:id>', views.edit),
    path('make_edit/<int:id>', views.make_edit),
    path('delete/<int:id>', views.delete),
    path('add_job/<int:id>', views.add_job_to_user),
]