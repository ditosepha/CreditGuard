from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Card
from time import time
import random
from django.urls import get_resolver

class CardAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user and authenticate the client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_card_number_validation(self):
        # Test card number validation by passing a card number with less than 16 digits. 
        url = reverse('cards-list')
        data = {
            'user': self.user.id,
            'title': 'Test Card',
            'card_number': '123456789112345', 
            'ccv': 334
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_card_number(self):
        # Test card number validation by passing card number with letters.
        url = reverse('cards-list')
        data = {
            'user': self.user.id,
            'title': 'Test Card',
            'card_number': '1234abcd5678efgh',
            'ccv': 334
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_ccv_validation(self):
        # Test CCV validation by passing a CCV with more than 3 digits.
        url = reverse('cards-list')
        data = {
            'user': self.user.id,
            'title': 'Test Card',
            'card_number': '123456789112345', 
            'ccv': 3344
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_performance(self):
        # Test the performance of the API by sending multiple POST requests.
        url = reverse('cards-list')
        request_num = 100

        card_numbers = [''.join([str(random.randint(0, 9)) for _ in range(16)]) for _ in range(request_num)]
        ccvs = [random.randint(100, 999) for _ in range(request_num)]

        start_time = time()

        for card_number, ccv in zip(card_numbers, ccvs):
            data = {
                'user': self.user.id,
                'title': 'Test Card',
                'card_number': card_number,
                'ccv': ccv
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        end_time = time()
        duration = end_time - start_time
        print(f"{request_num} POST request was processed in {duration} sec.")
        self.assertLess(duration, 5)