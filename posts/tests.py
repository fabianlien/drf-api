from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='john117', password='123')

    def test_can_list_posts(self):
        john117 = User.objects.get(username='john117')
        Post.objects.create(owner=john117, title='example title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='john117', password='123')
        response = self.client.post('/posts/', {'title': 'example title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthed_user_can_not_create_post(self):
        response = self.client.post('/posts/', {'title': 'example title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)