from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE)
    title = models.CharField(max_length=40)
    content = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def comment_count(self):
        return self.comments.all()
    
    def __str__(self):
        return str(self.title)+': '+str(self.author)
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    
    
class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #additional
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    comment_author=models.ForeignKey("auth.User",on_delete=models.CASCADE)
    comment_content=models.TextField(max_length=100)
    comment_date=models.DateTimeField(auto_now_add=True)