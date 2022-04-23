from rest_framework import serializers

from .models import User, PhoneNumber, Email


class CreateUserWithContactInfoSerializer(serializers.Serializer):
    lastname = serializers.CharField(max_length=255)
    firstname = serializers.CharField(max_length=255)
    emails = serializers.ListSerializer(child=serializers.EmailField())
    phonenumbers = serializers.ListSerializer(child=serializers.CharField())

    def create(self, validated_data):
        user = User.objects.create(lastname=validated_data["lastname"],
                                   firstname=validated_data["firstname"])
        for email in validated_data["emails"]:
            email_obj = Email.objects.create(email=email)
            user.emails.add(email_obj)
        for number in validated_data["phonenumbers"]:
            number_obj = PhoneNumber.objects.create(number=number)
            user.phonenumbers.add(number_obj)
        user.save()
        return user

    def to_representation(self, instance):
        _repr = dict()
        _repr["lastname"] = instance.lastname
        _repr["firstname"] = instance.firstname
        _repr["emails"] = [i.email for i in instance.emails.all()]
        _repr["phonenumbers"] = [i.number for i in instance.phonenumbers.all()]
        return _repr


class ListUsersSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    lastname = serializers.CharField(max_length=255)
    firstname = serializers.CharField(max_length=255)
    emails = serializers.ListSerializer(child=serializers.EmailField())
    phonenumbers = serializers.ListSerializer(child=serializers.CharField())

    def to_representation(self, instance):
        _repr = dict()
        _repr["id"] = instance.id
        _repr["lastname"] = instance.lastname
        _repr["firstname"] = instance.firstname
        _repr["emails"] = [i.email for i in instance.emails.all()]
        _repr["phonenumbers"] = [i.number for i in instance.phonenumbers.all()]
        return _repr
