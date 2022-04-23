from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Email, PhoneNumber
from .serializers import (CreateUserWithContactInfoSerializer,
                          ListUsersSerializer,
                          AddAdditionalContactInfoSerializer,
                          DetailedUserSerializer,
                          UpdateContactInfoSerializer,
                          DetailedEmailContactSerializer,
                          DetailedPhoneNumberContactSerializer,
                          UserDeleteSerializer)

from rest_framework.generics import GenericAPIView, ListAPIView


class UserView(GenericAPIView):
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'firstname']

    def post(self, request):
        serializer = CreateUserWithContactInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        qs = self.filter_queryset(User.objects.all())
        serializer = ListUsersSerializer(qs, many=True)
        return Response(serializer.data)

    def delete(self, request):
        serializer = UserDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(id=serializer.validated_data['id'])
            user.delete()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactInfoView(GenericAPIView):

    def post(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddAdditionalContactInfoSerializer(instance=user,
                                                        data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        try:
            qs = User.objects.get(id=kwargs['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DetailedUserSerializer(qs)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateContactInfoSerializer(instance=user,
                                                 data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetailedEmailContactView(ListAPIView):
    serializer_class = DetailedEmailContactSerializer
    queryset = Email.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            qs = User.objects.get(id=kwargs['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            email = qs.emails.get(pk=kwargs['pk'])
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(email)
        return Response(serializer.data)


class DetailedPhoneNumberContactView(ListAPIView):
    serializer_class = DetailedPhoneNumberContactSerializer
    queryset = PhoneNumber.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            qs = User.objects.get(id=kwargs['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            email = qs.phonenumbers.get(pk=kwargs['pk'])
        except PhoneNumber.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(email)
        return Response(serializer.data)
