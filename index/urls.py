from django.urls import path
from .views import login_views, register_views, index_views, logout_views

urlpatterns = [
    path('login/', login_views, name='login'),
    path('register/', register_views, name='register'),
    path('index/', index_views),
    path('logout/', logout_views, name='logout'),
]
