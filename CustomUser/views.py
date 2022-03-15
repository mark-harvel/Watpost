from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import generic
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from .models import Follow
from django.contrib.auth import get_user_model
from .forms import CustomUserProfileForm
from Blogs.models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class MyProfileView(generic.DetailView):

    """ Profile """

    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(MyProfileView, self).get_context_data(**kwargs)
        posts = self.object.blogposts.all()
        context['posts'] = posts
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != self.request.user:
            return redirect('profile', request.user.username, request.user.id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class EditProfile(LoginRequiredMixin, generic.UpdateView):

    """ Update the profile """

    model = get_user_model()
    template_name = 'users/edit.html'
    context_object_name = 'edit'
    form_class = CustomUserProfileForm

    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != self.request.user:
            return redirect('profile', request.user.username, request.user.id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class UserDetailView(generic.DetailView):

    """ User profile """

    model = get_user_model()
    template_name = 'users/user-detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        posts = self.object.blogposts.filter(status=1)
        context['posts'] = posts
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == self.request.user:
            return redirect('profile', request.user.username, request.user.id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


# Follow Actions
@ajax_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            recipient = get_user_model().objects.get(id=user_id)
            if action == 'follow':
                Follow.objects.get_or_create(user_from=request.user, user_to=recipient)
            else:
                Follow.objects.filter(user_from=request.user, user_to=recipient).delete()

            return JsonResponse({'status':'ok'})

        except:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})


class SubsView(LoginRequiredMixin, generic.ListView):

    """ Following posts """

    model = get_user_model()
    template_name = 'users/subs.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_user_model().objects.get(id=user_id)
        providers = user.following.all()
        queryset = BlogPost.objects.filter(author__in=providers)
        return queryset

