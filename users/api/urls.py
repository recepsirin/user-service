from django.urls import path
from .views import UserView, ContactInfoView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('users/<int:id>/contact/', ContactInfoView.as_view(), name='contact'),
]
