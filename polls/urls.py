from django.urls import path

from . import views

urlpatterns = [path('home/', views.get_home_page, name='home_page'),
               path('', views.get_home_page, name='home_page'),
               path('home/flotes/', views.get_flotes_page, name='flote_page'),
               path('home/flotes/<str:code>', views.get_flote_by_code, name='flote'),
               path('login', views.login_user, name='login'),
               path('logout', views.logout_user, name='logout'),
               path('flotes/add', views.add_flote, name='add_flote')
               ]
