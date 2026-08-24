from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from blog.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include("blog.urls")),
    path('login/', LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', register, name="register"),
    path('', include("blog.api_urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
