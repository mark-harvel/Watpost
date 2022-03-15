from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.generic.edit import FormMixin
from Blogs.forms import BlogPostForm, CommentForm
from django.views.decorators.http import require_POST
from Blogs.models import BlogPost, Topic, Comment
from django.core.paginator import Paginator
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class IndexView(generic.ListView):

    """ Default Home """

    queryset = BlogPost.objects.filter(status=1)
    context_object_name = 'posts'
    paginate_by = 30
    template_name = 'default/index.html'


class CreatePostView(LoginRequiredMixin, generic.CreateView):

    """ Create Posts """

    template_name = 'blog-posts/new-post.html'
    model = BlogPost
    form_class = BlogPostForm

    def form_valid(self, form):
        self.object =  form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogPostDetailView(FormMixin, generic.DetailView):

    """ Posts Detail """

    template_name = 'blog-posts/post-detail.html'
    model = BlogPost
    form_class = CommentForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        comments = self.object.comments.all()
        context['comments'] = comments
        context['form'] = self.get_form()
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        try:
            get_user_model().objects.get(id=request.user.id)
        except:
            return redirect('account_login')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.author = self.request.user
        new_comment.post = self.object
        new_comment.save()
        return super(BlogPostDetailView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')

    if post_id and action:
        try:
            post = BlogPost.objects.get(id=post_id)

            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


class UpdateBlogPostView(LoginRequiredMixin, generic.UpdateView):

    """ Update Post """

    model = BlogPost
    template_name = 'blog-posts/update-post.html'
    context_object_name = 'edit'
    form_class = BlogPostForm

    def get_context_data(self, **kwargs):
        context = super(UpdateBlogPostView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect('index')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class DeleteBlogPostView(LoginRequiredMixin, generic.DeleteView):

    """ Delete Post """

    model = BlogPost
    template_name = 'blog-posts/delete-post.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect('index')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_success_url(self):
        return self.object.author.get_absolute_url()


class CommentDelete(generic.DeleteView):

    """ Delete Comment """

    model = Comment
    context_object_name = 'comment'
    template_name = 'blog-posts/comment-delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class AllTopicView(generic.ListView):

    """ All topics """

    model = Topic
    template_name = 'blog-posts/all-topics.html'
    context_object_name = 'topics'

# topic list posts
def topic_posts(request, id):
    template_name = 'blog-posts/topic-posts.html'
    topic = get_object_or_404(Topic, id=id)
    posts = topic.blogposts.filter(status=1)
    paginator = Paginator(posts, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'topic': topic, 'posts': page_obj}

    return render(request, template_name, context)

# the list for particular tags
def tag_post(request, tag_slug=None): 
    template_name = 'blog-posts/tag-posts.html'
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = BlogPost.objects.filter(tags__in=[tag], status=1)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {'tag':tag, 'posts':page_obj}
    return render(request, template_name, context)

