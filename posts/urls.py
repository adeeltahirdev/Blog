from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:pk>/', views.post, name='post'),
    path('write/', views.write, name='write'),
    path('edit/<str:pk>/', views.edit, name='edit'),
    path('delete/<str:pk>/', views.delete, name='delete')
]