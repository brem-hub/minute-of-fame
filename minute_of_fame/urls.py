"""minute_of_fame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import include

from app import views

urlpatterns = [
    path('prototype/video-streaming/<int:num>', views.stream_test),
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('change_name/', views.change_name),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password-reset/reset/reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset/done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password-reset/confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password-reset/reset/done.html'),
         name='password_reset_complete'),
    path('', views.stream_page, name='index'),
    path('profile-settings/', views.profile_settings_page),
    path('about/', views.about_page),
    path('report/<int:badass_id>', views.report_page),
    path('profile_<str:id>/', views.profile_page),
    path('charts_data_<str:id>/', views.get_data_for_charts),
    path('top/', views.top_page),
    path('', include('social_django.urls', namespace='social'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

