from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='order_payment/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='order_payment/logout.html'), name='logout'),
]