from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Djalyarim')
        cls.user_unfollow = User.objects.create_user(username='Unfollow')
        cls.authorized_client = Client()
        cls.authorized_client_unfollow = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_unfollow.force_login(cls.user_unfollow)
        cls.group = Group.objects.create(
            title='future', description='про фьюче', slug='test_slug'
        )

        cls.post = Post.objects.create(
            text='Поле для текста',
            author=cls.user,
            group=cls.group,
        )
        cls.follow = Follow.objects.create(user=cls.user,
                                           author=cls.post.author)

    #  Проверка какой шаблон использует view функция
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('index'),
            'post_add.html': reverse('new_post'),
            'group.html': (reverse('group_posts',
                                   kwargs={'slug': 'test_slug'})),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    #  Проверка правильности переданого шаблона в контекст
    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    # Блок проверки контекста
    def test_index_list_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(reverse('index'))
        response_text = response.context['page'][0].text
        response_author = response.context['page'][0].author
        response_group = response.context['page'][0].group
        self.assertEqual(response_text, 'Поле для текста')
        self.assertEqual(response_author.username, 'Djalyarim')
        self.assertEqual(response_group.title, 'future')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test_slug'})
        )
        response_text = response.context['page'][0].text
        response_author = response.context['page'][0].author
        response_group = response.context['group']
        self.assertEqual(response_text, 'Поле для текста')
        self.assertEqual(response_author.username, 'Djalyarim')
        self.assertEqual(response_group.title, 'future')

    def test_username_post_edit_show_correct_context(self):
        """Шаблон /username/post/edit сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(
            reverse(
                'post_edit',
                kwargs={'username': self.user.username,
                        'post_id': self.post.id},
            )
        )
        response_text = response.context['post'].text
        response_author = response.context['post'].author
        response_group = response.context['post'].group
        self.assertEqual(response_text, 'Поле для текста')
        self.assertEqual(response_author.username, 'Djalyarim')
        self.assertEqual(response_group.title, 'future')

    def test_profile_show_correct_context(self):
        """Шаблон /profile/ сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        response_user = response.context['user'].username
        response_text = response.context['page'][0].text
        response_author = response.context['page'][0].author
        self.assertEqual(response_text, 'Поле для текста')
        self.assertEqual(response_author.username, 'Djalyarim')
        self.assertEqual(response_user, 'Djalyarim')

    def test_post_id_show_correct_context(self):
        """Шаблон username/post_id/ сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(
            reverse(
                'post', kwargs={'username': self.user.username,
                                'post_id': self.post.id}
            )
        )
        response_user = response.context['user'].username
        response_text = response.context['post'].text
        response_author = response.context['post'].author
        self.assertEqual(response_text, 'Поле для текста')
        self.assertEqual(response_author.username, 'Djalyarim')
        self.assertEqual(response_user, 'Djalyarim')

    # Блок проверки подписки
    def test_check_authorized_user_can_follow(self):
        """ Авторизованный пользователь может подписаться на автора """
        response = PostPagesTests.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        check_raise_follower = response.context['follower_count']
        self.assertEqual(check_raise_follower, 1)

    def test_check_authorized_user_can_unfollow(self):
        """ Авторизованный пользователь может отписаться от автора """
        Follow.objects.filter(user=self.user, author=self.post.author).delete()
        response = PostPagesTests.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        check_delete_follower = response.context['follower_count']
        self.assertEqual(check_delete_follower, 0)

    def test_check_new_post_appears_in_follow_index(self):
        """ Пост появляется в ленте подписчика """
        response = PostPagesTests.authorized_client.get(
            reverse('follow_index'))
        check_post = response.context['page'][0].text
        self.assertEqual(check_post, self.post.text)

    def test_check_new_post_dont_appears_in_follow_index(self):
        """ Пост не появляется в ленте подписчика """
        response = PostPagesTests.authorized_client_unfollow.get(
            reverse('follow_index'))
        check_post = response.context['page'].object_list
        self.assertFalse(check_post)

    # Блок комментариев
    def test_check_authorized_user_can_commens_post(self):
        """ Авторизованный клиент может оставлять комментарии """
        Comment.objects.create(text='Тестовый камментарий',
                               author=self.user, post=self.post)
        response = PostPagesTests.authorized_client.get(
            reverse(
                'post', kwargs={'username': self.user.username,
                                'post_id': self.post.id}
            )
        )
        comment = response.context['comments'][0].author
        self.assertEqual(comment, self.user)

    def test_check_unauthorized_user_cant_commens_post(self):
        """ Неавторизованный клиент не может оставлять комментарии """
        response = PostPagesTests.guest_client.get(
            reverse(
                'post', kwargs={'username': self.user.username,
                                'post_id': self.post.id}
            )
        )
        Comment.objects.create(text='Тестовый камментарий',
                               author=self.user, post=self.post)
        comment = response.context['comments']
        self.assertFalse(comment)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Джа')
        cls.group = Group.objects.create(
            title='future', description='про фьюче', slug='test_slug'
        )
        cls.post = Post.objects.create(
            text='Поле для текста', author=cls.user, group=cls.group
        )
        for step in range(12):
            Post.objects.create(
                text=f'Поле для текста {step}', author=cls.user,
                group=cls.group
            )
        cls.authorized_client = Client()

    def test_first_page_containse_ten_records(self):
        """ Проверяем количество постов на первой странице равно 10. """
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        """ Проверяем, что на второй странице должно быть три поста. """
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
