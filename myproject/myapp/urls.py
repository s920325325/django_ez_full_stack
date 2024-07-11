from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),  
    path('signup/', views.signup, name='signup'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('signup_failed/', views.signup_failed, name='sign_up_failed'),
    path('signin_success/', views.signin_success, name='signin_success'),
    path('stockdata/', views.display_stock_data, name='display_stock_data'),
]
