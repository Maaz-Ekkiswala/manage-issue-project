# Create your tests here.
from django.test import TestCase, Client
from apps.users.models import UserProfile


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = '/api/v1/users/signup/'
        self.login_url = '/api/v1/login/'
        self.user_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
            'mobile': '6565656565'
        }
        self.user_data_without_username = {
            'password': 'testpassword',
            'mobile': '6565656565'
        }
        self.user_data_incorrect_credentials = {
            'username': 'abc',
            'password': 'test'
        }

    def test_signup(self):
        # Send a POST request to the signup endpoint with the test user data
        response = self.client.post(self.signup_url, self.user_data)

        self.assertEqual(response.status_code, 201)

        self.assertTrue(UserProfile.objects.filter(username='testuser@example.com').exists())

    def test_signup_without_required_fields(self):
        response = self.client.post(self.signup_url, self.user_data_without_username)

        self.assertEqual(response.status_code, 400)

    def test_login(self):
        user = UserProfile.objects.create_user(**self.user_data)

        response = self.client.post(self.login_url, self.user_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue('access' and 'refresh' in response.json())

    def test_login_with_incorrect_credentials(self):
        response = self.client.post(self.login_url, self.user_data_incorrect_credentials)

        self.assertEqual(response.status_code, 401)