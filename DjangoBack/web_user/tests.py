
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
        self.admin_profile = Profile.objects.create(
            name="Admin",
            surnames="User",
            city="Admin City",
            postal_code="54321",
            phone="+987654321",
            birthdate="1990-01-01"
        )
        self.admin_user = User.objects.create_user(email="admin@example.com", password="adminpass", is_admin=True, profile = self.admin_profile)

        self.user_profile = Profile.objects.create(
            name="User",
            surnames="Example",
            city="User City",
            postal_code="12345",
            phone="+123456789",
            birthdate="2000-01-01"
        )
        self.user = User.objects.create_user(email="user@example.com", password="userpass", profile=self.user_profile)
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

        self.user_token = Token.objects.create(user=self.user)


    
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
        self.client.cookies['token'] = self.token.key

        data = {
            "password_old": "adminpass",
            "password_new": "newuserpass"
        }
        response = self.client.post(reverse('change_password'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(email="admin@example.com").check_password("newuserpass"))

    def test_logout(self):
        self.client.cookies['token'] = self.token.key
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Logout exitoso")
        self.assertTrue(response.cookies['token'].value == '')

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




    def test_info_profile(self):
        self.client.cookies['token'] = self.user_token.key

        response = self.client.get(reverse('info_profile'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.user.profile.name)
        self.assertEqual(response.data['surnames'], self.user.profile.surnames)
        self.assertEqual(response.data['city'], self.user.profile.city)
        self.assertEqual(response.data['postal_code'], self.user.profile.postal_code)
        self.assertEqual(response.data['phone'], self.user.profile.phone)
        self.assertEqual(response.data['birthdate'], str(self.user.profile.birthdate))


    def test_profile_update(self):
        self.client.cookies['token'] = self.user_token.key

        user_data = {
     
                "name": "Test",
                "surnames": "User",
                "city": "Test City",
                "postal_code": "1235",
                "phone": "+123456789",
                "birthdate": "2000-01-01"
 
        }

        response = self.client.put(reverse('update_profile'),data=user_data, format='json')
        self.assertEqual(response.status_code, 200)
        #Refrescar la BD
        self.user.refresh_from_db()
        self.user_profile.refresh_from_db()
        
        self.assertEqual(user_data["name"], self.user.profile.name)
        self.assertEqual(user_data["surnames"], self.user.profile.surnames)
        self.assertEqual(user_data["city"], self.user.profile.city)
        self.assertEqual(user_data["postal_code"], self.user.profile.postal_code)
        self.assertEqual(user_data["phone"], self.user.profile.phone)
        self.assertEqual(user_data["birthdate"], str(self.user.profile.birthdate))

