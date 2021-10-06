"""covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from detection import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Signup, Login, Logout
    path('login/', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),


    # Home Page, Current Page, Completed Page
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),


    # Update, Complete, Delete, Create
    path('detect/', views.makedetection, name='makedetect'),
    path('detection/<str:user_pk>', views.updatedata, name='updatedata'),
    path('detection/<str:user_pk>/delete', views.deletedata, name='deletedata'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
