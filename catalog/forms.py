from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Dress,Type,UserDetail
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.contrib.admin.widgets import AdminDateWidget
class BookDressForm(forms.Form):



    price = forms.IntegerField()
    daysno= forms.IntegerField(help_text="Enter the max number of days you will be keeping it for")
    reqdate=forms.DateField( widget=forms.widgets.DateInput(format="%m/%d/%Y"),help_text="Enter the date you will be needing it before the date")

        # Remember to always return the cleaned data.

    def clean(self):
        price = self.cleaned_data.get("price")
        daysno = self.cleaned_data.get("daysno")
        reqdate = self.cleaned_data.get("reqdate")

        return self.cleaned_data
class BuyDressForm(forms.Form):


    Buyno = forms.IntegerField(help_text="Enter Value less than 10")



    def clean(self):
        buyno = self.cleaned_data.get("Buyno")

        return self.cleaned_data
class AddDressForm(forms.Form):

    name=forms.CharField()
    type=forms.ModelChoiceField(queryset=Type.objects.all())
    dress_pic=forms.ImageField()
    dress_pic2=forms.ImageField(required=False)
    detail= forms.CharField()
    price = forms.IntegerField()
    rentday = forms.IntegerField()




    def clean(self):
        name = self.cleaned_data.get("name")
        type = self.cleaned_data.get("type")
        detail = self.cleaned_data.get("detail")
        price = self.cleaned_data.get("price")
        dress_pic = self.cleaned_data.get("dress_pic")
        dress_pic2 = self.cleaned_data.get("dress_pic2")
        rentday = self.cleaned_data.get("rentday")

        return self.cleaned_data
class AddTransactionForm(forms.Form):

    price = forms.IntegerField()
    daysno= forms.IntegerField(help_text="Enter the max number of days the user will be keeping it for")
    reqdate=forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"),help_text="Enter the date the fine limit days start")

    def clean(self):
        price = self.cleaned_data.get("price")
        daysno = self.cleaned_data.get("daysno")
        reqdate = self.cleaned_data.get("reqdate")

        return self.cleaned_data
class AddFinalForm(forms.Form):

    fine = forms.IntegerField()
    insuranceclaimstatus=forms.BooleanField()
    def clean(self):
        fine = self.cleaned_data.get("fine")
        insuranceclaimstatus = self.cleaned_data.get("insuranceclaimstatus")


        return self.cleaned_data
class AddTypeForm(forms.Form):

    name=forms.CharField()

    type_pic=forms.ImageField()
    detail= forms.CharField()





    def clean(self):
        name = self.cleaned_data.get("name")

        detail = self.cleaned_data.get("detail")

        type_pic = self.cleaned_data.get("type_pic")

        return self.cleaned_data
class UserCreateForm(ModelForm):


    password2 = forms.CharField(widget=forms.PasswordInput(),help_text="Confirm Password")
    location = forms.CharField()
    contact_info = forms.CharField()

    def clean(self):

        cleaned_data=super(UserCreateForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        validators.validate_password(password=password,user=username)

        if password != password2:
            raise forms.ValidationError("The two password fields must match. Got it!!??")
        return cleaned_data
    def save(self):
         # create new user
        new_user=User.objects.create_user(username=self.cleaned_data['username'],
                                    first_name=self.cleaned_data['first_name'],
                                    last_name=self.cleaned_data['last_name'],
                                    password=self.cleaned_data['password'],
                                    email=self.cleaned_data['email'],
                                    is_superuser=self.cleaned_data['is_superuser'],
                                        )
        m1=UserDetail(user=new_user,location=self.cleaned_data.get('location'),contact_info=self.cleaned_data.get('contact_info'))
        m1.save()
        return new_user

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','is_superuser')
class UserinfoChangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(UserinfoChangeForm, self).__init__(*args, **kwargs)

    username=forms.CharField(max_length=191)
    first_name=forms.CharField(max_length=191)
    last_name=forms.CharField(max_length=191)
    email=forms.EmailField()
    location = forms.CharField()
    def clean(self):

        cleaned_data=super(UserinfoChangeForm, self).clean()
        username = cleaned_data.get('username')
        userlist=User.objects.exclude(username=self.user.username).values_list('username', flat=True)
        print (userlist)
        if username in userlist:
            raise ValidationError(_('Account with this username already exists'))

        return cleaned_data
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
