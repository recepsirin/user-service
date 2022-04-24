from django.test import TestCase
from model_mommy import mommy
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
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


class BaseAPITest(TestCase):
    def __int__(self):
        self.client = APIClient()

    def setUp(self):
        self._test_generate_users()

    def _test_generate_users(self):
        for i in range(1, 11):
            mommy.make(User, id=i, emails=[mommy.make(Email)],
                       phonenumbers=[mommy.make(PhoneNumber)])


class UsersEndpointTest(BaseAPITest):

    def setUp(self):
        super(UsersEndpointTest, self).setUp()
        self.payload = {
            "lastname": "Doe", "firstname": "John",
            "emails": ["john.doe@gmail.com", "noname@domain.com"],
            "phonenumbers": ["+90 555 555 55 55", "+49 555 55 55"]
        }

    def test_create_user_with_contact_info(self):
        response = self.client.post(reverse('user'), self.payload,
                                    content_type="application/json",
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), self.payload)

    def test_list_users(self):
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertIsInstance(response.json()[0], dict)

    def test_delete_user(self):
        response = self.client.delete(reverse('user'), {"id": 1},
                                      content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(reverse('user'), {"id": 2121},
                                      content_type="application/json",
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactInfoEndpointTest(BaseAPITest):

    def setUp(self):
        super(ContactInfoEndpointTest, self).setUp()
        self.payload = {
            "email": "john.doe@gmail.com",
            "phone_number": "+90 555 555 55 55"
        }

    def test_add_additional_contact_info(self):
        # api/v1/users/1/contact/
        response = self.client.post(reverse('contact', kwargs={'id': 1}),
                                    {
                                        "emails": ["john.doe@gmail.com",
                                                   "noname@domain.com"],
                                    },
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # there are currently no any record with the id is 123 on db
        response = self.client.post(reverse('contact', kwargs={'id': 123}),
                                    self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(reverse('contact', kwargs={'id': 1}),
                                    self.payload,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # return data will be whole contact info from the related user
        returned_data = response.json()
        self.assertEqual(returned_data['emails'][-1], self.payload['email'])
        self.assertEqual(returned_data['phonenumbers'][-1],
                         self.payload['phone_number'])

    def test_list_specific_users_contact_info(self):
        # api/v1/users/1/contact
        response = self.client.get(reverse('contact', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.json()
        self.assertEqual(user_data['id'],
                         1)  # kwargs data above which refers user's id
        self.assertIn("lastname", user_data)
        self.assertIn("firstname", user_data)
        self.assertIn("emails", user_data)
        self.assertIn("phonenumbers", user_data)

        response = self.client.get(reverse('contact', kwargs={'id': 141}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_users_contact_info(self):
        # api/v1/users/1/contact/
        will_be_updated = {"emails": ["recepsirin@gmail.com",
                                      "asdadasd@mail.com"],
                           "phonenumbers": ["+90 0555 777 22 11"]
                           }
        response = self.client.put(reverse('contact', kwargs={'id': 1}),
                                   will_be_updated, format='json',
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(will_be_updated, response.json())


class TestDetailedEmailContactView(BaseAPITest):
    def setUp(self):
        super(TestDetailedEmailContactView, self).setUp()

    def test_detailed_contact_email(self):
        # api/v1/users/1/contact/email/1
        response = self.client.get(reverse('email', kwargs={'id': 1,
                                                            'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=1)
        email = user.emails.all()[0].email  # emails => 1st item => email data
        self.assertEqual(response.json()['email'], email)

        # api/v1/users/1/contact/email/11112
        response = self.client.get(reverse('email', kwargs={'id': 1,
                                                            'pk': 11112}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # api/v1/users/12/contact/email/1
        response = self.client.get(reverse('email', kwargs={'id': 12,
                                                            'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDetailedPhoneNumberContactView(BaseAPITest):
    def setUp(self):
        super(TestDetailedPhoneNumberContactView, self).setUp()

    def test_detailed_contact_phone_number(self):
        # api/v1/users/1/contact/phone-number/1
        response = self.client.get(reverse('number', kwargs={'id': 1,
                                                             'pk': 1}),
                                   headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=1)
        phone_number = user.phonenumbers.all()[0].number
        self.assertEqual(response.json()['number'], phone_number)

        # api/v1/users/1/contact/phone-number/11112
        response = self.client.get(reverse('number', kwargs={'id': 1,
                                                             'pk': 11112}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # api/v1/users/12/contact/phone-number/1
        response = self.client.get(reverse('number', kwargs={'id': 12,
                                                             'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
