from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from .models import Activity, Document, Nino, Mayor, Lider, Monitor, Parent, InscriptionBase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token


User = get_user_model()

class ActivityTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email="admin@example.com", password="adminpass", is_admin=True)
        self.client.force_authenticate(user=self.admin_user)

        self.user = User.objects.create_user(email="user@example.com", password="userpass")
        
        self.activity = Activity.objects.create(
            name='Test Activity', 
            adress='Test Address', 
            date_start='2023-01-01', 
            date_end='2023-01-02', 
            hours_start='10:00', 
            price='100', 
            packing_list='Test Packing List', 
            family_reunion='Test Family Reunion', 
            there_are_meting=False
        )

    def test_create_activity(self):
        url = reverse('create_activity')
        data = {
            'name': 'New Activity', 
            'adress': 'New Address',
            'date_start': '2024-01-01',
            'date_end': '2024-01-02',
            'hours_start': '10:00',
            'price': '200',
            'packing_list': 'New Packing List',
            'family_reunion': 'New Family Reunion',
            'there_are_meting': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'success')

    def test_update_activity(self):
        url = reverse('update_activity', kwargs={'activity_id': self.activity.id})
        data = {
            'name': 'Updated Activity', 
            'adress': 'Updated Address',
            'date_start': '2023-02-01',
            'date_end': '2023-02-02',
            'hours_start': '11:00',
            'price': '150',
            'packing_list': 'Updated Packing List',
            'family_reunion': 'Updated Family Reunion',
            'there_are_meting': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Activity')



    def test_get_activity(self):
        url = reverse('get_activity', kwargs={'activity_id': self.activity.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Activity')

    def test_delete_activity(self):
        url = reverse('delete_activity', kwargs={'activity_id': self.activity.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Actividad eliminada exitosamente')

    def test_all_activities(self):
        url = reverse('all_activities')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)


class InscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email="admin@example.com", password="adminpass", is_admin=True)

        self.user = User.objects.create_user(email="user@example.com", password="userpass")

        self.activity = Activity.objects.create(
            name='Test Activity', 
            adress='Test Address', 
            date_start='2023-01-01', 
            date_end='2023-01-02', 
            hours_start='10:00', 
            price='100', 
            packing_list='Test Packing List', 
            family_reunion='Test Family Reunion', 
            there_are_meting=False
        )

        self.activity_second = Activity.objects.create(
            name='Second Activity', 
            adress='Second Address', 
            date_start='2023-01-01', 
            date_end='2023-01-02', 
            hours_start='10:00', 
            price='100', 
            packing_list='Second Test Packing List', 
            family_reunion='Second Test Family Reunion', 
            there_are_meting=True
        )

        # Crear archivos simulados para los documentos
        health_card_content = b'health card content'
        self.health_card = SimpleUploadedFile('health_card.txt', health_card_content, content_type='text/plain')

        pago_content = b'pago content'
        self.pago = SimpleUploadedFile('pago.txt', pago_content, content_type='text/plain')

        criminal_offenses_certificate_content = b'criminal_offenses_certificate content'
        self.criminal_offenses_certificate = SimpleUploadedFile('criminal_offenses_certificate.txt', criminal_offenses_certificate_content, content_type='text/plain')

        sexual_crimes_certificate_content = b'sexual_crimes_certificate content'
        self.sexual_crimes_certificate = SimpleUploadedFile('sexual_crimes_certificate.txt', sexual_crimes_certificate_content, content_type='text/plain')

        cisv_safeguarding_content = b'cisv_safeguarding content'
        self.cisv_safeguarding = SimpleUploadedFile('cisv_safeguarding.txt', cisv_safeguarding_content, content_type='text/plain')


        self.token = Token.objects.create(user=self.admin_user)

        self.user_token = Token.objects.create(user=self.user)


    def test_ninos_inscription(self):
        url = reverse('ninos_inscription')
        self.client.cookies['token'] = self.user_token.key
        data = {
            'activity': self.activity.id,
            'rol': 'ninos',
            'allergy': 'None',
            'image_authorization': True,
            'emergency_phone': '+123456789',
            't_shirt_size': 'M',
            'medicines': 'None',
            'health_card': self.health_card,
            'pago': self.pago,
            'status': 0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Nino.objects.count(), 1)
        nino = Nino.objects.get()
        self.assertEqual(nino.user, self.user)
        self.assertEqual(nino.activity, self.activity)


    def test_mayores_inscription(self):
        url = reverse('mayores_inscription')
        self.client.cookies['token'] = self.user_token.key
        data = {
            'activity': self.activity_second.id,
            'rol': 'mayores',
            'image_authorization': True,
            'emergency_phone': '+123456789',
            't_shirt_size': 'L',
            'health_card': self.health_card,
            'pago': self.pago,
            'status': 0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Mayor.objects.count(), 1)
        mayor = Mayor.objects.get()
        self.assertEqual(mayor.user, self.user)
        self.assertEqual(mayor.activity, self.activity_second)
        

    def test_lider_inscription(self):
        url = reverse('lider_inscription')
        self.client.cookies['token'] = self.user_token.key
        data = {
            'activity': self.activity.id,
            'rol': 'lider',
            'dni' : '12345678Q',
            'profession': 'doctor',
            'languages': 'castellano',
            'image_authorization': True,
            'emergency_phone': '+123456789',
            't_shirt_size': 'L',
            'sexual_crimes_certificate': self.sexual_crimes_certificate,
            'criminal_offenses_certificate': self.criminal_offenses_certificate,
            'health_card': self.health_card,
            'cisv_safeguarding': self.pago,
            'status': 0
        }
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lider.objects.count(), 1)
        lider = Lider.objects.get()
        self.assertEqual(lider.user, self.user)     
        self.assertEqual(lider.activity, self.activity)


    def test_monitor_inscription(self):
        url = reverse('monitor_inscription')
        self.client.cookies['token'] = self.user_token.key
        data = {
            'activity': self.activity.id,
            'rol': 'monitor',
            'image_authorization': True,
            'emergency_phone': '+123456789',
            'dni' : '12345678Q',
            'languages': 'castellano',
            't_shirt_size': 'L',
            'sexual_crimes_certificate': self.sexual_crimes_certificate,
            'criminal_offenses_certificate': self.criminal_offenses_certificate,
            'health_card': self.health_card,
            'cisv_safeguarding': self.cisv_safeguarding,
            'pago': self.pago,
            'status': 0
        }
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Monitor.objects.count(), 1)
        monitor = Monitor.objects.get()
        self.assertEqual(monitor.user, self.user)
        self.assertEqual(monitor.activity, self.activity)

    def test_parent_inscription(self):
        url = reverse('parent_inscription')
        self.client.cookies['token'] = self.user_token.key
        data = {
            'activity': self.activity_second.id,
            'sexual_crimes_certificate': self.health_card,
            'profession': 'doctor',
            'criminal_offenses_certificate': self.criminal_offenses_certificate,
            'cisv_safeguarding': self.cisv_safeguarding,
            'pago': self.pago,
            'status': 0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Parent.objects.count(), 1)
        parent = Parent.objects.get()
        self.assertEqual(parent.user, self.user)
        self.assertEqual(parent.activity, self.activity_second)


    def test_get_inscription(self):
        self.test_ninos_inscription()  # Crear una inscripción primero
        url = reverse('get_inscription', args=[self.activity.id, self.user.email, 'ninos'])
        self.client.cookies['token'] = self.token.key
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['emergency_phone'], '+123456789')
        self.assertEqual(response.data['t_shirt_size'], 'M')



    def test_accept_inscription(self):
        # Primero crear una inscripción
        self.test_ninos_inscription()
        nino = Nino.objects.get()
        url = reverse('accept_inscription', args=[nino.id])
        self.client.cookies['token'] = self.token.key
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        nino.refresh_from_db()
        self.assertEqual(nino.status, 1) 

    def test_reject_inscription(self):
        # Primero crear una inscripción
        self.test_ninos_inscription()
        nino = Nino.objects.get()
        url = reverse('reject_inscription', args=[nino.id])
        self.client.cookies['token'] = self.token.key
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        nino.refresh_from_db()
        self.assertEqual(nino.status, 2)

    def test_all_inscriptions(self):
        # Crear algunas inscripciones
        self.test_ninos_inscription()
        self.test_mayores_inscription()

        url = reverse('all_inscriptions',  args=[self.activity.id])
        self.client.cookies['token'] = self.token.key  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        inscriptions = response.data
        self.assertEqual(len(inscriptions), 1)


    def test_user_inscriptions(self):
        # Crear algunas inscripciones

        self.test_ninos_inscription()
        self.test_mayores_inscription()

        url = reverse('user_inscriptions')
        self.client.cookies['token'] = self.user_token.key  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        inscriptions = response.data
        self.assertEqual(len(inscriptions), 2)
