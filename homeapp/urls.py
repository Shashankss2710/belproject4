from django.conf import settings
from django.urls import path
from . import views
from .views import Home
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),  #we need a url for uploading
    path('like-post', views.like_post, name='like-post'), 
    path('search/', views.search, name='search'),  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)