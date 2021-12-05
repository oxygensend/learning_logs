from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.test.client import Client
# Create your tests here.

# Check if user after registration is logged properly
# Chec if user is logged properly
# Check if user is logged out after 


def createUser(username, password):

    return User.objects.create_user(username=username, password=password)


# class RegistrationViewTest(TestCase):

    
#     def test_that_user_is_logged_in(self):
#         response = self.client.post(reverse('users:register'), 
#                                 { 'username':'foo', 
#                                   'password1':'bar', 
#                                   'password2':'bar' }  
#                                 )    
                    
#         user = auth.get_user(self.client)
#         print(response.context['user'])
#         self.assertTrue(user.is_authenticated)