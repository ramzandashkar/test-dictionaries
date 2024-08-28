from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from .models import Dictionary, DictionaryElement, DictionaryVersion


class DictionaryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.dictionary = Dictionary.objects.create(code='test_dict',
                                                    name='Test Dictionary')
        self.version1 = DictionaryVersion.objects.create(
            dictionary=self.dictionary, version='1.0',
            start_date=timezone.now() - timezone.timedelta(days=10))
        self.version2 = DictionaryVersion.objects.create(
            dictionary=self.dictionary, version='2.0',
            start_date=timezone.now() + timezone.timedelta(days=10))
        self.element = DictionaryElement.objects.create(version=self.version1,
                                                        code='001',
                                                        value='Example')

    def test_get_dictionaries_no_date(self):
        response = self.client.get('/refbooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refbooks', response.data)
        self.assertEqual(len(response.data['refbooks']), 1)

    def test_get_dictionaries_with_date(self):
        response = self.client.get('/refbooks/?date=2024-08-30')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refbooks', response.data)
        self.assertEqual(len(response.data['refbooks']), 1)

    def test_get_dictionaries_invalid_date(self):
        response = self.client.get('/refbooks/?date=invalid_date')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "error": "Неверный формат даты. Используйте ГГГГ-ММ-ДД."})

    def test_get_dictionary_elements(self):
        response = self.client.get(f'/refbooks/{self.dictionary.id}/elements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('elements', response.data)
        self.assertEqual(len(response.data['elements']), 1)

    def test_get_dictionary_elements_with_version(self):
        response = self.client.get(
            f'/refbooks/{self.dictionary.id}/elements/?version=1.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('elements', response.data)
        self.assertEqual(len(response.data['elements']), 1)

    def test_check_element_exists(self):
        response = self.client.get(
            f'/refbooks/{self.dictionary.id}/check-element/'
            f'?code=001&value=Example')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"exists": True})

    def test_check_element_not_exists(self):
        response = self.client.get(
            f'/refbooks/{self.dictionary.id}/check-element/'
            f'?code=002&value=Nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"exists": False})

    def test_check_element_with_version(self):
        response = self.client.get(
            f'/refbooks/{self.dictionary.id}/check-element/'
            f'?code=001&value=Example&version=1.0')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"exists": True})

    def test_check_element_version_not_found(self):
        response = self.client.get(
            f'/refbooks/{self.dictionary.id}/check-element/'
            f'?code=001&value=Example&version=nonexistent_version')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"exists": False})
