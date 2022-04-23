from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import User
from .serializers import (CreateUserWithContactInfoSerializer,
                          ListUsersSerializer)

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
