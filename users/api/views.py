from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import User
from .serializers import (CreateUserWithContactInfoSerializer,
                          ListUsersSerializer,
                          AddAdditionalContactInfoSerializer,
                          DetailedUserSerializer,
                          UpdateContactInfoSerializer, )

from rest_framework.generics import GenericAPIView


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
