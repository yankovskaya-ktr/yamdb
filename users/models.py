from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserRole:
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    CHOICES = (
        (UserRole.USER, 'user'),
        (UserRole.MODERATOR, 'moderator'),
        (UserRole.ADMIN, 'admin'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль в системе',
        max_length=30,
        choices=CHOICES,
        default=UserRole.USER
    )
    email = models.EmailField('Email', unique=True)

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR

    class Meta:
        ordering = ['username']

    def __str__(self):
        if self.username:
            return self.username
        return self.email
