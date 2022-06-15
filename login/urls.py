from django.contrib import admin
from django.urls import path
from user_login.views import sign_up, login_view, refresh_token_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('signup/', sign_up, name='sign_up'),
    path('login/', login_view, name='token_obtain_pair'),
    path('refreshtoken/', refresh_token_view, name='token_refresh'),
    path('logout/', logout_view, name='logout')
]