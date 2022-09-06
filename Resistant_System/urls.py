from django.urls import path
from . import views

urlpatterns = [
    path('upload_yes_i_need/', views.upload_page, name='upload_page'),
    path('remove_yes_i_need/', views.reloadData, name='reload'),

    path('data/<int:page>/', views.data, name='data'),
    path('species/', views.species, name='special'),
    path('system/', views.system, name='system'),
    path('mes/', views.mes, name='message'),


    path('download/', views.download, name='download'),
    path('upload_csv/<int:type>/', views.upload_csv, name='upload_csv'),

    path('test/', views.join_table)
]