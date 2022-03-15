from django.contrib.auth.models import AbstractUser
from django.db import models
import django
from django.urls.base import reverse
from django.conf import settings
import uuid


class Follow(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='is_following', on_delete=models.CASCADE)

    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='is_followed', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username', db_index=True)
    picture = models.ImageField(blank=True, upload_to='user-pictures/%Y%m/%d')
    about = models.TextField(blank=True)
    following = models.ManyToManyField('self', through=Follow, related_name='followers', symmetrical=False)
    private = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username, 'pk': str(self.id)})

