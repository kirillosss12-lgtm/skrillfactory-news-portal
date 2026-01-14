from django.urls import path
from .views import UserUpdate, upgrade_me

urlpatterns = [
    path('profile/', UserUpdate.as_view(), name='user_edit'),
    path('upgrade/', upgrade_me, name='upgrade'),
]