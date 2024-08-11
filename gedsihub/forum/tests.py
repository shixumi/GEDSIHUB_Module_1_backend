# lmshub/chatbot/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FAQ

class FAQTests(APITestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(question='What is LMSHub?', answer='A learning management system hub.')

    def test_faq_list(self):
        response = self.client.get('/chatbot/faqs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_faq_detail(self):
        response = self.client.get(f'/chatbot/faqs/{self.faq.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], 'What is LMSHub?')
