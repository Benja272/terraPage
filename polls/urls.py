from django.urls import path

from . import views

urlpatterns = [path('flote/<str:name>', views.get_flote_by_name, name='flote_name'),
               path('home/', views.get_home_page, name='home_page'),
               path('home/flotes/', views.get_flotes_page, name='flote_page'),
               path('login', views.login_user, name='login'),
               path('logout', views.logout_user, name='logout'),
               path('home/flotes/add', views.add_flote, name='add_flote')
               ]
