from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'reg'),
    path('search/', views.search, name = 'search'),
    path('logout/', views.logout_f, name = 'logout_f'),
    path('<int:chat_id>/', views.chat, name = 'chat')
]
