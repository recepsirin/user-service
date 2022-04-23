from django.urls import path
from .views import (UserView, ContactInfoView, DetailedEmailContactView,
                    DetailedPhoneNumberContactView)

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('users/<int:id>/contact/', ContactInfoView.as_view(), name='contact'),
    path('users/<int:id>/contact/email/<int:pk>',
         DetailedEmailContactView.as_view(), name='email'),
    path('users/<int:id>/contact/phone-number/<int:pk>',
         DetailedPhoneNumberContactView.as_view(), name='number'),
]
