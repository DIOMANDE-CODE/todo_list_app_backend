from django.urls import path
from .views import reset_password, change_password

urlpatterns = [
    path('reset-password/', reset_password, name='reset-password'),
    path('reset-password-confirm/<int:uid>/<str:token>/', change_password, name='reset-password-confirm')
]