from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.generate_prescription, name='index'),  # this name is critical!
    path('verify/', views.verify_prescription, name='verify_prescription'),
    path('success/', views.success_page, name='success_page'),
]
