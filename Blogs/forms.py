from django import forms
from Blogs.models import BlogPost, Comment
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('poster', 'title', 'is_nsfw', 'topic', 'content', 'status', 'tags')
        widgets = {
            'content': SummernoteWidget()
        }

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['topic'].widget.attrs = {'class':'form-select mb-3'}
        self.fields['tags'].widget.attrs = {'class':'form-control'}
        self.fields['is_nsfw'].widget.attrs = {'class':'form-check mb-3'}
        self.fields['is_nsfw'].label = '+18 NFSW'
        self.fields['poster'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['content'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['status'].widget.attrs = {'class':'form-control mb-3'}
 
 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = 'Comment'
        self.fields['content'].widget.attrs = {'class':'form-control mb-3'}
