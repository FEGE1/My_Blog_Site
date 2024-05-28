from django import forms
from .models import Post,UserModel,Comment
from django.contrib.auth.models import User

class UserMainForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirmPassword=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')
    
    def clean(self):
        username=self.cleaned_data.get("username")
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        confirmPassword=self.cleaned_data.get("confirmPassword")

        if password and confirmPassword and password != confirmPassword:
            raise forms.ValidationError("Password Unmatched!")
        else:
            values={
                "username":username,
                "password":password,
                "email":email,
            }
            return values
    
class UserForm(forms.ModelForm):
   
    class Meta:
        model = UserModel
        fields = ('profile_pic',)

class UserloginForm(forms.Form):
    username=forms.CharField(label="Username:")
    password=forms.CharField(label="Password:",widget=forms.PasswordInput)

class PostUpdateForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('title','content')

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment_content',)