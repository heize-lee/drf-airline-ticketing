# # backend/accounts/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('login/', views.login, name='login'),
#     path('delete/<int:uid>/', views.delete_user, name='delete_user'),
#     path('change-password/', views.change_password, name='change_password'),
# ]

from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup')
]