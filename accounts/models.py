"""Models for Topsy content."""

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from . import entities


class UserManager(BaseUserManager):
    """Helper functions for users."""

    def from_entity(self, entity):
        return self.model(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            last_login=entity.last_login,
            status=entity.status
        )


class User(AbstractBaseUser):
    """User account."""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField()
    modified_at = models.DateField()
    last_login = models.DateField(null=True)
    status = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.modified_at = timezone.now()

        super().save(*args, **kwargs)

    def to_entity(self):
        return entities.User(
            id=self.id,
            email=self.email,
            name=self.name,
            created_at=self.created_at,
            modified_at=self.modified_at,
            last_login=self.last_login,
            status=self.status
        )
