from django.urls import path
from . import views # views.py file
#  '.' means the root directory

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/',views.about, name='about' )
]
