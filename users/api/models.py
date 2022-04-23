from django.db import models


class Email(models.Model):
    email = models.EmailField(max_length=1024)


class PhoneNumber(models.Model):
    number = models.CharField(max_length=24)


class User(models.Model):
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    emails = models.ManyToManyField('api.Email', default=[])
    phonenumbers = models.ManyToManyField('api.PhoneNumber', default=[])
