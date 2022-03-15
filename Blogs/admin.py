from django.contrib import admin
from .models import Topic, BlogPost

class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ('title', 'slug',)
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Topic, TopicAdmin)
admin.site.register(BlogPost)