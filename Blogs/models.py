from django.db import models
import uuid
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls.base import reverse
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(blank=True, upload_to='topic/%Y%m/%d')
    
    class Meta:
        ordering =['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( 'topic', kwargs={ 'slug': str(self.slug)})


class BlogPost(models.Model):
    STATUS = [
        (0, 'Draft'),
        (1, 'Publish')
    ]

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogposts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250)
    poster = models.ImageField(upload_to='blogposters/%Y/%m/%d')
    topic = models.ForeignKey(Topic, related_name='blogposts', on_delete=models.CASCADE)
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)
    is_nsfw = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_post_liked', blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={ 'slug': self.slug, 'pk':str(self.id) })

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author} commented {self.content}'
