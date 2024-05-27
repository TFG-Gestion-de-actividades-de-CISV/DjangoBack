
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from web_user.models import Web_User_Pending, Profile
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email="admin@example.com", password="adminpass", is_admin=True)
        self.user = User.objects.create_user(email="user@example.com", password="userpass")
        self.pending_user = Web_User_Pending.objects.create(
            email="pending@example.com",
            password="pendingpass",
            profile=Profile.objects.create(
                name="Pending",
                surnames="User",
                city="Test City",
                postal_code="12345",
                phone="+123456789",
                birthdate="2000-01-01"
            )
        )
        self.token = Token.objects.create(user=self.admin_user)

    
    def test_login_user(self):
        user = User.objects.create_user(email="testuser@example.com", password="password123")
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.cookies)

   

    def test_registration_requests(self):
        self.client.cookies['token'] = self.token.key
        response = self.client.get(reverse('registration_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("email" in response.data[0])

    
    def test_change_password(self):
        data = {
            "email": "user@example.com",
            "password_old": "userpass",
            "password_new": "newuserpass"
        }
        response = self.client.post(reverse('change_password'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(email="user@example.com").check_password("newuserpass"))

    def test_logout(self):
        self.client.cookies['token'] = self.token.key
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Logout exitoso")

    def test_register_new_user(self):
        user_data = {
            "email": "testuser@example.com",
            "password": "password123",
            "profile": {
                "name": "Test",
                "surnames": "User",
                "city": "Test City",
                "postal_code": "12345",
                "phone": "+123456789",
                "birthdate": "2000-01-01"
            }
        }
        response = self.client.post(reverse('register'), user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Web_User_Pending.objects.filter(email="testuser@example.com").exists())
    
    def test_reject_request(self):
        self.client.cookies['token'] = self.token.key
        data = {
            "email": "pending@example.com",
            "reason": "Invalid information"
        }
        response = self.client.post(reverse('reject_request'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Web_User_Pending.objects.filter(email="pending@example.com").exists())




    def test_accept_request(self):
        self.client.cookies['token'] = self.token.key
        data = {
            "email": "pending@example.com"
        }
        response = self.client.post(reverse('acept_request'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="pending@example.com").exists())
        self.assertFalse(Web_User_Pending.objects.filter(email="pending@example.com").exists())
