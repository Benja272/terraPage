from django.urls import path

from . import views

urlpatterns = [
            path('home/', views.get_home_page, name='home_page'),
            path('', views.get_home_page, name='home_page'),
            path('home/flotes/', views.get_flotes_page, name='flote_page'),
            path('home/flotes/null', views.get_flotes_page, name='flote_page'),
            path('home/flotes/<str:code>', views.get_flote_by_code, name='flote'),
            path('login', views.login_user, name='login'),
            path('logout', views.logout_user, name='logout'),
            path('flotes/add', views.add_flote, name='add_flote'),
            path('home/flotes/add_repair/<str:code>', views.add_repair, name='add_repair'),
            path('home/flotes/repair/<str:code>', views.list_repair, name='repair'),
            path('delete/flote/<str:code>', views.delete_flote, name='delete_flote'),
            path('delete/repair/<str:pk>', views.delete_repair, name='delete_repair'),
            path('delete/img/<str:pk>', views.delete_img, name='delete_img'),
            path('alerts/<str:code>', views.alerts, name='alerts'),
            ]
