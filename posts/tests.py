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

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='john117', password='123')
        response = self.client.post('/posts/', {'title': 'example title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthed_user_can_not_create_post(self):
        response = self.client.post('/posts/', {'title': 'example title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        john = User.objects.create_user(username='john117', password='123')
        cortana = User.objects.create_user(username='cortana', password='123')
        Post.objects.create(owner=john, title='example title', content='Spartan stuff')
        Post.objects.create(owner=cortana, title='example title', content='AI stuff')

    def test_user_can_retrieve_a_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'example title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_a_post_without_id(self):
        response = self.client.get('/posts/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_user_posts(self):
        self.client.login(username='john117', password='123')
        response = self.client.put('/posts/1/', {'title': 'Updated title'})
        self.assertEqual(response.data['title'], 'Updated title')

    def test_user_cannot_update_other_user_posts(self):
        self.client.login(username='cortana', password='123')
        response = self.client.put('/posts/1/', {'title': 'Updated title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
