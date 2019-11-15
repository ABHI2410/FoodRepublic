from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home,name = 'FoodRepublic-home'),
    path('rest/<str:rest_name>',views.rest,name = 'FoodRepublic-rest'),
    path('login/',auth_views.LoginView.as_view(template_name='FoodRepublic/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='FoodRepublic/logout.html'),name='logout'),
    path('register/',views.register,name='register'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('cart/',views.cart,name='cart'),
    path('result/',views.result,name='result')
]
