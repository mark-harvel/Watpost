from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'picture', 'first_name', 'last_name', 'email', 'about',)

    def __init__(self, *args, **kwargs):
        super(CustomUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class':'form-control'} 
        self.fields['picture'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['first_name'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['last_name'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['email'].widget.attrs = {'class':'form-control mb-3'}
        self.fields['about'].widget.attrs = {'class':'form-control mb-3'}             
    
 
