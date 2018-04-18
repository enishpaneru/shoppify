from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from db_file_storage.model_utils import delete_file, delete_file_if_needed
# Create your models here.
from django import template
register = template.Library()
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Dress(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=24)
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    dress_pic = models.FileField(upload_to='images/dresspics/', blank=True, null=True)
    dress_pic2 = models.FileField(upload_to='images/dresspics/', blank=True, null=True,default=None)
    detail = models.TextField(max_length=1000, help_text="Enter a brief description of the dress")
    price = models.PositiveIntegerField(blank=True)
    date = models.DateField(null=True, blank=True)
    search_index=models.PositiveIntegerField(default=9,blank=True)
    search_indexval=models.FloatField(default=9,blank=True)
    rentday=models.PositiveIntegerField(blank=True,help_text="Days of rent you would allow")
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["-name"]


    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('dress-detail', args=[str(self.id)])




import uuid

class DressInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular Dress.")
    dress = models.ForeignKey('Dress', null=True)
    imprint = models.CharField(max_length=200)








    class Meta:
        ordering = ["id"]
        permissions = (("can_mark_returned", "Set book as returned"),)



    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.dress.name)
class Type(models.Model):

    name = models.CharField(max_length=100)
    detail = models.TextField(max_length=200,null=True)
    type_pic = models.ImageField(upload_to='images/typepics/', blank=True, null=True)



    def get_absolute_url(self):

        return reverse('type-detail', args=[str(self.id)])


    def __str__(self):

        return '%s' % (self.name)
class booking(models.Model):

    user = models.ForeignKey(User)
    dress = models.ForeignKey(Dress)
    bookdate=models.DateField(null=True, blank=True)
    price = models.PositiveIntegerField()
    daysno= models.PositiveIntegerField(help_text="Enter the max number of days you will be keeping it for")
    reqdate=models.DateField(null=True, blank=True,help_text="Enter the date you will be needing it before the date")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.dress.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('bookno-detail', args=[str(self.id)])

class OrderDetail(models.Model):

    dress = models.ForeignKey('Dress', null=True)
    orderno=models.IntegerField()
    orderuser=models.ForeignKey('Order', null=True)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s' % (self.id)
class Order(models.Model):

    user = models.ForeignKey(User)
    orderdate=models.DateField(null=True, blank=True)
    active=models.BooleanField(default=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.user)
class UserDetail(models.Model):
    contact_info=models.CharField(max_length=14)
    user = models.ForeignKey(User)
    location=models.TextField(null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.user)
class transaction(models.Model):

    renter = models.ForeignKey(User)

    dress = models.ForeignKey(Dress)
    transactiondate=models.DateField(null=True, blank=True)
    price = models.PositiveIntegerField()
    daysno= models.PositiveIntegerField(help_text="Enter the max number of days the user will be keeping it for")
    reqdate=models.DateField(null=True, blank=True,help_text="Enter the date the fine limit days start")
    active = models.BooleanField(default=False)
    completion=models.BooleanField(default=False)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.dress.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('bookno-detail', args=[str(self.id)])
class rentinfo(models.Model):



    transaction = models.ForeignKey(transaction)

    fine = models.PositiveIntegerField()

    insuranceclaimstatus=models.BooleanField(default=False)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.transaction.id


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('bookno-detail', args=[str(self.id)])
class tempimage(models.Model):

    dress_pic = models.FileField(upload_to='images/dresspics/', blank=True, null=True)


    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('dress-detail', args=[str(self.id)])
