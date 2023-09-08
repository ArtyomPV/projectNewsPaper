from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

# Create your models here.


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.author_name.username}'

    def update_rating(self):
        postRat = self.post_set.all().aggregate(posting=Sum('rating_post'))
        pRat = 0
        pRat += postRat.get('posting')

        commRat = self.author_name.comment_set.all().aggregate(commenting=Sum(
            'rating_comment'))
        cRat = 0
        cRat += commRat.get('commenting')

        self.rating = 3 * pRat + cRat + 2
        self.save()


class Post(models.Model):
    NEWS = 'NW'
    POST = 'PT'
    POSTS = [
        (NEWS, 'news'),
        (POST, 'post')
    ]
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name='Автор')
    post_type = models.CharField(
        max_length=2, choices=POSTS, default=NEWS, verbose_name='Тип статьи')
    data_post_creation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField()
    rating_post = models.IntegerField(default=0)
    category = models.ManyToManyField('Category', through='PostCategory')

    def __str__(self):
        return f'Post #{self.pk} - Name: {self.title}'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на
    def get_absolute_url(self):
        # страницу с товаром
        return f'/posts/{self.id}'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, default='History')
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
    def get_category(self):
        return self.name
    
    class Meta:
        verbose_name = 'Наименование категории'
        verbose_name_plural = 'Наименование категорий'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_comment = models.IntegerField(default=0)
    text_comment = models.TextField()
    data_comment_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author_comment.username

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'