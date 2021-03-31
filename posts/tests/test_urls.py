from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Djalyarim')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user_2 = User.objects.create_user(username='Djalyarim2')
        cls.authorized_client_2 = Client()
        cls.authorized_client_2.force_login(cls.user_2)
        cls.another_author = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_2.force_login(cls.user_2)
        cls.group = Group.objects.create(
            title='future', description='про фьюче', slug='test_slug'
        )

        cls.post = Post.objects.create(
            text='Поле для текста',
            author=cls.user,
            group=cls.group,
        )

    #  Блок проверки доступа неавторизованных пользователей
    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_slug_page_unauthorized(self):
        """Страница /group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test_slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_author_unauthorized(self):
        """Страница /about/author доступна любому пользователю."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_tech_unauthorized(self):
        """Страница /about/tech доступна любому пользователю."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    #  Блок проверки ошибок
    def test_error_404(self):
        """ Страница не найдена """
        response = self.guest_client.get('/wrong/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    #  Блок профайла
    def test_profile_authorized(self):
        """Страница profile доступна авторизованному пользователю."""
        response = PostURLTests.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_guest(self):
        """Страница profile доступна неавторизованному пользователю."""
        response = PostURLTests.guest_client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_post_id_authorized(self):
        """Страница profile/post_id доступна авторизированному пользователю."""
        response = PostURLTests.authorized_client.get(
            reverse(
                'post', kwargs={'username': self.user.username,
                                'post_id': self.post.id}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_post_id_guest(self):
        """ Страница profile/post_id доступна неавторизированному """
        """ пользователю. """
        response = PostURLTests.guest_client.get(
            reverse(
                'post', kwargs={'username': self.user.username,
                                'post_id': self.post.id}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_post_id_edit_authorized_and_author(self):
        """Страница profile/post_id/edit доступна только авторизированному """
        """ пользователю и только автору поста"""
        response = PostURLTests.authorized_client.get(
            reverse(
                'post_edit',
                kwargs={'username': self.user,
                        'post_id': self.post.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_post_id_edit_authorized_not_author(self):
        """Страница profile/post_id/edit не доступна авторизированному """
        """ пользователю и не автору поста"""
        response = PostURLTests.authorized_client_2.get(
            reverse(
                'post_edit',
                kwargs={'username': self.user_2,
                        'post_id': self.post.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_profile_post_id_edit_guest(self):
        """Страница profile/post_id/edit не доступна не авторизированному """
        """ пользователю """
        response = PostURLTests.guest_client.get(
            reverse(
                'post_edit',
                kwargs={'username': self.user,
                        'post_id': self.post.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    #  Блок проверки доступа авторизованных пользователей
    def test_post_new_page_authorized(self):
        """Страница /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    #  Блок проверки редиректов для неавторизованных пользователей
    def test_add_page_redirect(self):
        """Страница /new/ перенаправляет неавторизованного пользователя."""
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_post_edit_redirect(self):
        """Страница username/post_id/edit перенаправляет
        неавторизованного пользователя."""
        response = PostURLTests.guest_client.get(
            reverse(
                'post_edit',
                kwargs={'username': self.user.username,
                        'post_id': self.post.id},
            ),
            follow=True,
        )
        self.assertRedirects(
            response, '/auth/login/?next=%2FDjalyarim%2F1%2Fedit%2F')

    #  Блок проверки ожидаемых шаблонов
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test_slug/',
            'post_add.html': reverse(
                'post_edit',
                kwargs={'username': self.user.username,
                        'post_id': self.post.id},
            ),
        }

        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
