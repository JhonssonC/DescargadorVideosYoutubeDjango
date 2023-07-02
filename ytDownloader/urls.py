from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('resolutions/', views.getResolution, name='resolution'),
]