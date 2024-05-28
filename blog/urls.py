from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
app_name='blog'

urlpatterns = [
    path('create/',views.PostCreate.as_view(),name="create"),
    path('delete/<int:id>',views.PostDelete,name='delete'),
    path('update/<int:id>',views.PostUpdate,name='update'),
    path('comment_delete/<int:id>',views.CommentDelete,name='comment_delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)