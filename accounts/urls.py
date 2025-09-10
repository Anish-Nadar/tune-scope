from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('password_reset_phone/', views.password_reset_phone, name='password_reset_phone'),
    path('password_reset_verify_otp/', views.password_reset_verify_otp, name='password_reset_verify_otp'),
    path('password_reset_confirm_new/', views.password_reset_confirm_new, name='password_reset_confirm_new'),
]
