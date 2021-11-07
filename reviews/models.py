from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """
    Категории произведений
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры произведений
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения
    """
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField('Год создания')
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Связующая таблица произведение - жанр.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'], name='unique_genre_title'
            ),
        ]
        verbose_name = 'Произведене-жанр'

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'


class Review(models.Model):
    """
    Отзывы на произведения
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='one_review_from_one_author'
            ),
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Комментарии к отзывам
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарии'
