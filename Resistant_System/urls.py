from django.urls import path
from . import views

urlpatterns = [
    path('reload', views.reloadData, name='reload'),
    path('data', views.data, name='data'),
    path('species', views.species, name='special'),
    path('system', views.system, name='system'),
    path('download', views.download, name='download')
]