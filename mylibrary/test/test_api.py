from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from mylibrary.models import Book
from mylibrary.serializers import BookSerializer

class BookApiTest(APITestCase):
    def test_get_list(self):
        goods=Book.objects.create(title='яичница', price=680)
        response = self.client.get(reverse('api_list'))
        serial=BookSerializer([goods,], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial, response.data)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        url = reverse('api_list')
        data = {'title': 'Это Тест', 'author': 'Ivanov','description': '', 'price': 0.0}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_delete_book(self):
        data = Book.objects.create(title='Это Тест', author='Ivanov',description='', price=0.0)
        url = reverse('api_detail', kwargs={'pk': data.pk})
        response = self.client.delete(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)


    def test_update_list(self):
        goods=Book.objects.create(title='золушка', author='Bro',description='', price=1.0)
        response = self.client.get(reverse('api_list'))
        data = {'title': 'Это Тест', 'author': 'Ivanov', 'description': '', 'price': 0.0}
        url = reverse('api_detail', kwargs={'pk': goods.pk})
        response = self.client.put(url, data=data)
        goods.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(goods.title, data['title'])
