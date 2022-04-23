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


class AddAdditionalContactInfoSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=1024)
    phone_number = serializers.CharField(max_length=24)

    def update(self, instance, validated_data):
        email = Email.objects.create(email=validated_data['email'])
        instance.emails.add(email)
        number = PhoneNumber.objects.create(
            number=validated_data['phone_number'])
        instance.phonenumbers.add(number)
        return instance

    def to_representation(self, instance):
        _repr = dict()
        _repr["emails"] = [i.email for i in instance.emails.all()]
        _repr["phonenumbers"] = [i.number for i in instance.phonenumbers.all()]
        return _repr



class UpdateContactInfoSerializer(serializers.Serializer):
    emails = serializers.ListSerializer(child=serializers.EmailField())
    phonenumbers = serializers.ListSerializer(child=serializers.CharField())

    def update(self, instance, validated_data):
        instance.emails.clear()
        instance.phonenumbers.clear()
        for email in validated_data["emails"]:
            email_obj = Email.objects.create(email=email)
            instance.emails.add(email_obj)
        for number in validated_data["phonenumbers"]:
            number_obj = PhoneNumber.objects.create(number=number)
            instance.phonenumbers.add(number_obj)
        instance.save()
        return instance

    def to_representation(self, instance):
        _repr = dict()
        _repr["emails"] = [i.email for i in instance.emails.all()]
        _repr["phonenumbers"] = [i.number for i in instance.phonenumbers.all()]
        return _repr


class DetailedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        _repr = dict()
        _repr["id"] = instance.id
        _repr["lastname"] = instance.lastname
        _repr["firstname"] = instance.firstname
        _repr["emails"] = {i.id: i.email for i in instance.emails.all()}
        _repr["phonenumbers"] = {i.id: i.number for i in instance.phonenumbers.all()}
        return _repr
