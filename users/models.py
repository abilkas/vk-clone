from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("E-Mail must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    sex_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField('День рождения', null=True, blank=True)
    sex = models.CharField(max_length=6, choices=sex_choices)
    is_email_verifed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(
        _('is deleted'),
        default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @classmethod
    def create_superuser(cls, email, password):
        superuser = cls.objects.create_superuser(email=email, password=password

        )
    @classmethod
    def create_user(cls, email, password=None, first_name=None, last_name=None,
                    birth_date=None):

        if datetime.today() - birth_date < 13:
            raise ValidationError(
                _('Вам должно быть больше 13')
            )

        user = cls.objects.create_user(email, password=password, first_name=first_name,
                                       last_name=last_name,
                                       birth_date=birth_date)

        return user

    # def count_posts(self):
    #     return self.posts.count()

    def __str__(self):
        return self.email

    def update_email(self, email):
        if self.email == email:
            raise ValidationError
        else:
            self.email = email
            self.save()

    def update_password(self, password):
        if self.password == password:
            raise ValidationError
        else:
            self.set_password(password)
            self.save()

    def update_first_name(self, first_name):
        self.first_name = first_name
        self.save()

    def update_last_name(self, last_name):
        self.last_name = last_name
        self.save()

    def update_birth_date(self, birth_date):
        if self.birth_date == birth_date:
            raise ValidationError
        else:
            self.birth_date = birth_date
            self.save()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'following_user_id', )

    @classmethod
    def create_follow(cls, user_id, following_user_id):
        follow = UserFollowing.objects.create(user_id=user_id, following_user_id=following_user_id)

        return follow