from django.test import TestCase
from model_mommy import mommy
from rest_framework.exceptions import ValidationError

from .models import User, Email, PhoneNumber
from .serializers import CreateUserWithContactInfoSerializer


class UserModelTest(TestCase):

    def setUp(self):
        self.user = mommy.make(User, emails=[mommy.make(Email)],
                               phonenumbers=[mommy.make(PhoneNumber)])

    def test_model_relations(self):
        self.assertEqual(type(self.user.firstname), str)
        self.assertEqual(type(self.user.lastname), str)
        self.assertIsInstance(self.user.emails.all()[0], Email)
        self.assertIsInstance(self.user.phonenumbers.all()[0], PhoneNumber)
        self.assertEqual(type(self.user.emails.all()[0].email), str)
        self.assertEqual(type(self.user.phonenumbers.all()[0].number), str)

        self.user.emails.clear()
        self.assertIsNotNone(self.user.emails.all())
        self.assertEqual(len(self.user.emails.all()), 0)


class CreateUserWithContactInfoSerializerTest(TestCase):
    def setUp(self):
        self.payload = {
            "lastname": "Doe", "firstname": "John",
            "emails": ["john.doe@gmail.com", "noname@domain.com"],
            "phonenumbers": ["+90 555 555 55 55", "+49 555 55 55"]
        }
        self.user = mommy.make(User, emails=[mommy.make(Email)],
                               phonenumbers=[mommy.make(PhoneNumber)])

    def _validate(self):
        serializer = CreateUserWithContactInfoSerializer(data=self.payload)
        serializer.is_valid(raise_exception=True)

    def test_serializer_isvalid_ok(self):
        self._validate()

    def test_lastname_validation(self):
        self.payload.pop("lastname")
        with self.assertRaises(ValidationError):
            self._validate()

    def test_firstname_validation(self):
        self.payload.pop("firstname")
        with self.assertRaises(ValidationError):
            self._validate()

    def test_contact_info_validation(self):
        self.payload.pop("emails")
        with self.assertRaises(ValidationError):
            self._validate()

    def test_representation(self):
        serializer = CreateUserWithContactInfoSerializer(data=self.payload)
        serialized_response_data = serializer.to_representation(self.user)

        self.assertIn("lastname", serialized_response_data)
        self.assertIn("firstname", serialized_response_data)
        self.assertIn("emails", serialized_response_data)
        self.assertIn("phonenumbers", serialized_response_data)
        self.assertIsInstance(serialized_response_data, dict)
        self.assertIsInstance(serialized_response_data['emails'], list)
        self.assertIsInstance(serialized_response_data['phonenumbers'], list)

    def test_saved_instance(self):
        serializer = CreateUserWithContactInfoSerializer(data=self.payload)
        serializer.is_valid(True)
        serializer.save()
        _instance = User.objects.get(firstname="John")

        self.assertEqual(_instance.firstname, self.payload['firstname'])
        self.assertEqual(_instance.lastname, self.payload['lastname'])
        self.assertEqual(_instance.emails.all()[0].email,
                         self.payload['emails'][0])
        self.assertEqual(_instance.phonenumbers.all()[0].number,
                         self.payload['phonenumbers'][0])
