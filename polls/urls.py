from django.urls import path

from . import views

urlpatterns = [path('flote/<str:name>',views.get_flote_by_name_view,name='flote_name'),
               path('flote/',views.get_flotes_view, name='flote'),
               path('home/',views.get_home_page, name='home_page'),
               path('home/flotes',views.get_flotes_page, name='flote_page')
                ]