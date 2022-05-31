from django.contrib.auth import get_user_model
from django.db.models.fields import json
from django.test import TestCase
from django.urls import reverse
from .models import User, Artist, Comment, Category


class WebsiteTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret'
        )

        self.user = User.objects.create(
            username='username',
            email='username@gmail.com',
            password='password',
        )

        self.category = Category.objects.create(
            name='rappers',
            slug='rappers',
        )

        self.artist = Artist.objects.create(
            name='John',
            nick='Eminem',
            slug='eminem',
            image='photos/2022/05/28/og-buda.jpg',
            content='Worst rapper',
            category=self.category,
        )

        self.comment = Comment.objects.create(
            post=self.artist,
            user=self.user,
            content='new comment',
        )

    def test_string_representation(self):
        self.assertEqual(str(self.artist), self.artist.nick)
        self.assertEqual(str(self.category), self.category.name)

    def test_get_absolute_url(self):
        self.assertEqual(self.artist.get_absolute_url(), reverse('post', kwargs={'post_slug': self.artist.slug}))

    def test_artist_content(self):
        self.assertEqual(f'{self.artist.name}', 'John')
        self.assertEqual(f'{self.artist.nick}', 'Eminem')
        self.assertEqual(f'{self.artist.slug}', 'eminem')
        self.assertEqual(f'{self.artist.content}', 'Worst rapper')
        self.assertEqual(f'{self.artist.category}', 'rappers')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post', kwargs={'post_slug': self.artist.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post.html')

    def test_category_detail_view(self):
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('addpost'), {
            'name': 'name',
            'nick': 'nick',
            'slug': 'nick',
            'content': 'new ontent',
            'category': 'rappers',
        })
        self.assertEqual(response.status_code, 200)

    def test_post_edit_view(self):
        response = self.client.post(reverse('edit', kwargs={'post_slug': self.artist.slug}), {
            'content': 'new content',
        })
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        response = self.client.post(reverse('delete', kwargs={'post_slug': self.artist.slug}))
        self.assertEqual(response.status_code, 302)
