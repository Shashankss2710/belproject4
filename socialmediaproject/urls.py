"""socialmediaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#we import one url for each app and in our app folder we specify our different urls and path goes on views app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profileapp.urls')),   
    path('', include('registrationapp.urls')),
    path('', include('homeapp.urls')),     
    path('settings/', include('settingsapp.urls')),    #this is allow only if there is only one url in apps


]


urlpatterns = urlpatterns+static(settings.MEDIA_URL, 
 document_root=settings.MEDIA_ROOT)