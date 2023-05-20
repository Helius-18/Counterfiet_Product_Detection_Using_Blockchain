"""fake_product_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appname import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('manufacturer/retailer_signup/', views.create_retailer, name='retailer_signup'),
    path('manufacturer/dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),
    path('manufacturer/new_product/', views.add_product, name='newproduct'),
    path('retailer/dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
    path('retailer/verify_product/', views.verify_product, name='verify_product'),
    path('execute/',views.executer,name="tester"),
    path("qrcode/<str:data>",views.qrcode,name="qrcode"),
    path('consumer/dashboard/', views.consumer_dashboard, name='consumer_dashboard'),
]
