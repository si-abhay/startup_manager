"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from home.views import (
    home,
)
from startups.views import (
    register,
    profile,
    update_profile,
    view_profile,
    payment_page,
    payment_cancelled,
    payment_done,
    grievances_view,
    submit_request,
    reg_final,
    blog,
    blogsingle,
    blog_category,
    blog_tag,
    create_blog,
    
)

from filter.views import (
    info,
    get_districts_view,
)

urlpatterns = [
    #change admin login view and this url note:1
    path('admin/login/', auth_views.LoginView.as_view(template_name='startups/admin_login.html'), name='admin_login'),
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('grievances/', grievances_view, name='grievances'),
    path('login/', auth_views.LoginView.as_view(template_name='startups/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='startups/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='startups/password_reset.html'), name='password_reset'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='startups/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='startups/password_change_done.html'), name='password_change_done'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='startups/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='startups/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='startups/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('view_profile/', view_profile, name='view_profile'),
    path('payment_page/', payment_page, name='payment_page'),
    path('payment_cancelled/',payment_cancelled, name='payment_cancelled'),
    path('payment_done/', payment_done, name='payment_done'),
    path('submit-request/', submit_request, name='submit_request'),

    path('reg_final/', reg_final, name='reg_final'),

    path('info/', info, name='info'),
    path('get-districts/', get_districts_view, name='get_districts'),
    path('blog/', blog, name='blog'),
    path('blogsingle/', blogsingle, name='blogsingle'),

    path('category/<int:category_id>/', blog_category, name='category'),
    path('tag/<int:tag_id>/', blog_tag, name='tag'),
    path('create_blog/', create_blog, name='create_blog'),

]

urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = "StartupManager Admin"
admin.site.site_title = "Startup Admin Portal"  