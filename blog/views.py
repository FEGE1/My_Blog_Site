from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from . import models
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import UserForm,UserMainForm,UserloginForm
from django.shortcuts import redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse,reverse_lazy
from .forms import PostUpdateForm,CommentCreateForm

# class IndexView(ListView):
#     template_name='index.html'
    
#     model=models.Post
#     context_object_name='posts'
    
#     def get_context_data(self, **kwargs) -> dict[str, Any]:
#         current_user=request.user
#         user_id=current_user.id
#         context = super().get_context_data(**kwargs) 
#         context["deneme"] = 'as'
#         return context

def IndexView(request): 
    posts=models.Post.objects.all().order_by('-create_date')
 
    context={'posts':posts,}
       
    return render(request,'index.html',context)

def UserRegister(request):
        if request.method=='POST':
            userMain=UserMainForm(data=request.POST)
            userForm=UserForm(files=request.FILES)

            if userMain.is_valid() and userForm.is_valid()  :
                user=userMain.save()
                user.set_password(user.password)
                user.save()

                profile=userForm.save(commit=False)
                profile.user=user
                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']
                
                profile.save()

                login(request,user)
            else:
                print(userForm.errors)
        else:
            userMain=UserMainForm()
            userForm=UserForm()
        
        return render(request,'blog/registration.html',{'userForm':userForm,'userMain':userMain})

def UserLogin(request):
    UserLoginForm=UserloginForm(data=request.POST or None)

    if UserLoginForm.is_valid():
        username=UserLoginForm.cleaned_data.get("username")
        password=UserLoginForm.cleaned_data.get("password")

        user=authenticate(username=username,password=password)

        if user:
            login(request,user)
            return redirect('index')
        else:
            return redirect('index')

    context={'UserLoginForm':UserLoginForm}
    return render(request,'blog/login.html',context)
def UserLogout(request):
    logout(request)
    return redirect('index')

def BlogDetailView(request,pk):

    if request.method=='POST':
        if request.user.is_authenticated:
            commentForm=CommentCreateForm(request.POST)
            post=models.Post.objects.get(pk=pk)
            if commentForm.is_valid():
                comment=commentForm.save(commit=False)
                comment.comment_author=request.user
                comment.post=post
                comment.save()

                return HttpResponseRedirect(request.path_info)

            else:
                return HttpResponse('Form is not valid !')
        else:
            return HttpResponse('You must log in if you want to post a comment.')        
    else:
 
        post=models.Post.objects.get(pk=pk)
        comments=post.comments.all().order_by('-comment_date')
        commentForm=CommentCreateForm()


        return render(request,'blog/blog_details.html',context={'post':post,'comments':comments,'form':commentForm})

@login_required
def UserProfile(request):
    if request.user.is_authenticated:
        profile_pic=models.UserModel.objects.filter(user=request.user)
        return render(request,'blog/profile.html',{'UserModel':profile_pic})
    else:
        return HttpResponse("You need to Login for view profile page.")

@login_required
def Dashboard(request):
    if request.user.is_authenticated:
        UserPosts=models.Post.objects.filter(author_id=request.user).order_by('-create_date')
        return render(request,'blog/dashboard.html',context={'posts':UserPosts})   
    else:
        return HttpResponse("You need to Login for view profile page.")

class PostCreate(CreateView):
    template_name='blog/post_create.html'
    model=models.Post
    fields=('title','content')

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def PostUpdate(request,id):
    UserPost=models.Post.objects.get(author_id=request.user,id=id)
    if request.method=='POST':

        form=PostUpdateForm(request.POST,request.FILES,instance=UserPost)  
        
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            
            return redirect('dashboard')
        else:
            return HttpResponse('Form is Not valid !')

    else:
        form=PostUpdateForm(instance=UserPost)
    return render(request,'blog/post_update.html',{'form':form})


@login_required    
def PostDelete(request,id):
    post=models.Post.objects.get(author_id=request.user,id=id)
    if not post:
        return HttpResponse("Permission Denied !")
    else:
        if request.method=='POST':
            post.delete()
            return redirect('dashboard')
        else:

            return render(request,'blog/post_delete.html',{'post':post})
@login_required
def CommentDelete(request,id):
    comment=models.Comment.objects.get(comment_author_id=request.user,id=id)
    if not comment:
        return HttpResponse("Permission Denied !")
    else:
        if request.method=='POST':
            comment.delete()
            return redirect('index')
        else:

            return render(request,'blog/comment_delete.html',{'comment':comment})