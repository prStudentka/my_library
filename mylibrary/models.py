import datetime
from django.utils.timezone import now
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Category(models.Model):
    CategoryType = models.TextChoices('CategoryType', 'Сказки Сборники Классика Научно-популярные Справочники Другое')
    name = models.CharField(max_length=80,
                            verbose_name='Наименование категории',
                            choices=CategoryType.choices,
                            )
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Book(models.Model):
    CoverType = models.TextChoices('CoverType', 'Твёрдый Мягкий Интегральный Картонный')
    Book_Sizes = (
        ('A4', '210 х 297'),
        ('A5', '145 x 205'),
        ('A6', '102 х 142'),
        ('A7', '74 х 105'),
    )
    title = models.CharField('Название', max_length=60)
    author = models.CharField('Автор', max_length=30, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    pages = models.PositiveIntegerField('Страниц', default=4)
    price = models.FloatField('Цена', default=0.0)
    type_cover = models.CharField('Тип обложки', choices=CoverType.choices, max_length=18, blank=True)
    size = models.CharField('Размер',max_length=2, choices=Book_Sizes)
    date_public = models.DateField('Дата публикации', default=datetime.date.today())
    picture = models.ImageField("Картинка", upload_to='image/', blank=True)
    exist = models.BooleanField('В наличии?', default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return "Книга: "+self.title

    class Meta:
        verbose_name="Книга"
        verbose_name_plural="Книги"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.pk})


class Comment(models.Model):
    theme = models.CharField(max_length=60, verbose_name='Тема', help_text="Тема, проблема")
    nickname = models.CharField(max_length=30, verbose_name='Ник')
    text = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='Книга')

    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)

    class Meta:
        verbose_name="Комментарий"
        verbose_name_plural="Комментарии"

    def __str__(self):
        return "Комментарий: "+self.theme

    def get_absolute_url(self):
        return reverse('info_com_view', kwargs={'comment_id': self.pk})

class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(default=now, verbose_name='Дата создания')
    books = models.ManyToManyField(Book, related_name='+',)
    CategoryType = models.TextChoices('CategoryType', 'Передано Ожидает Собирается')
    status = models.CharField(max_length=80, verbose_name='Статус', choices=CategoryType.choices, default='Собирается')

    class Meta:
        verbose_name="Корзина"
        verbose_name_plural="Корзины"
