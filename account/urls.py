from . import views
from django.urls import path

urlpatterns=[
    path('login/', views.user_login, name='login'),
    path('register/', views.register_user, name='register'),
    path('update/', views.update_user, name='update_user'),
    path('delete/',views.delete_user, name='delete_user'),
]
