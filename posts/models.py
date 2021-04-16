from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name='Заголовок')
    text = models.TextField(help_text='Создайте здесь свой пост',
                            verbose_name='Пост')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='Группа',
        null=True,
        related_name='posts',
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Картинка')

    class Meta:
        ordering = ('-pub_date', 'id')

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField('date published', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')


class Profile_id(models.Model):
    text_profile = models.TextField(blank=True, null=True, verbose_name='Поле для текста')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_img')
    image_author = models.ImageField(upload_to='users/', blank=True, verbose_name='Ваша аватарка')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='liker')
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='liking')
