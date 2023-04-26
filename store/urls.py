from django.urls import path

from . import views
from .views import Main, Cart, CheckOut, store, Login, Signup, logout
#from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Main.as_view(), name = 'homepage'),
    path('store/',store, name='store'),
    path('cart/', Cart.as_view(), name='cart'),
    path('home',views.home, name='home'),
    path('checkout', CheckOut.as_view(), name='checkout'),
    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup' ),
    path('logout',logout, name='logout')
]