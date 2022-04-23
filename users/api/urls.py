from django.urls import path
from .views import UserView, ContactInfoView, DetailedEmailContactView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('users/<int:id>/contact/', ContactInfoView.as_view(), name='contact'),
    path('users/<int:id>/contact/list/email/<int:pk>',
         DetailedEmailContactView.as_view(), name='email'),

]
