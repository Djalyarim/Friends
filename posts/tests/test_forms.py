import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Djalyarim')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='future', description='про фьюче', slug='test_slug'
        )

        cls.post = Post.objects.create(
            text='Первая запись',
            author=cls.user,
            group=cls.group,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        """ Удалаем временные папки"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """ В базе данных создана новая запись черeз форму PostForm"""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='very_small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Поле для текста',
            'author': 'Джа',
            'image': uploaded
        }

        self.authorized_client.post(reverse('new_post'),
                                    data=form_data, follow=True)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_change_post(self):
        """ В базе данных изменена запись черeз форму PostForm"""
        form_data = {
            'text': 'Вторая запись',
            'author': 'Джа',
        }
        response = PostPagesTests.authorized_client.post(
            reverse(
                'post_edit',
                kwargs={'username': self.user.username,
                        'post_id': self.post.id}
            ),
            data=form_data,
            follow=True,
        )
        response_change = response.context['post'].text
        self.assertNotEquals(response_change, self.post.text)

    #  Блок проверки контекста на содержание картинок
    def test_check_context_contains_image_index(self):
        response = PostPagesTests.authorized_client.post(
            reverse('index'))
        self.assertTrue(response.context['page'][0].image)

    def test_check_context_contains_image_profile(self):
        response = PostPagesTests.authorized_client.post(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertTrue(response.context['page'][0].image)

    def test_check_context_contains_image_group(self):
        response = PostPagesTests.authorized_client.post(
            reverse('group_posts', kwargs={'slug': 'test_slug'}))
        self.assertTrue(response.context['page'][0].image)

    def test_check_context_contains_image_post(self):
        response = PostPagesTests.authorized_client.post(
            reverse('post', kwargs={'username': self.user.username,
                                    'post_id': self.post.id}))
        self.assertTrue(response.context['post'].image)

    def test_index_cache(self):
        """ Проверка данных из Cache страницы index"""
        response_first = PostPagesTests.authorized_client.post(
            reverse('index')).templates
        cache.clear()
        response_second = PostPagesTests.authorized_client.post(
            reverse('index')).templates
        self.assertNotEqual(response_first, response_second)
