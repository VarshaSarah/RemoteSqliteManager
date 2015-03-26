from django.db import models

# Create your models here.


class SystemDetails(models.Model):
    hostname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ipaddress = models.CharField(max_length=15)


class DbDetails(models.Model):
    dbpath = models.CharField(max_length=200)


class QueryDetails(models.Model):
    query = models.CharField(max_length=200)