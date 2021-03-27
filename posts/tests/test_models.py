from django.contrib.auth.models import User
from django.test import TestCase

from posts.models import Group, Post


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Бессмыслица',
            author=User.objects.create(username='Джа')
        )
        cls.group = Group.objects.create(title='future',
                                         description='про фьюче',
                                         slug='test_slug')

    def test_title_help_text(self):
        """help_text поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        helpText = post._meta.get_field('text').help_text
        self.assertEquals(helpText, 'Создайте здесь свой пост')

    def test_title_vebrose_name(self):
        """Vebrose_name полей text, group совпадает с ожидаемыми."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Пост',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_object_name_is_title_field_Post(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = PostModelTest.post
        expected_object_name = post.text
        self.assertEquals(expected_object_name, str(post))

    def test_object_name_is_title_field_Group(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))
