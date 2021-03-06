"""Uebung6 URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from Useradmin.views import HomeBirthdayView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home", permanent="false")),
    path("admin/", admin.site.urls),
    path("home/", HomeBirthdayView.as_view(template_name="home.html"), name="home"),
    path("useradmin/", include("Useradmin.urls")),
    path("useradmin/", include("django.contrib.auth.urls")),
    path("games/", include("Games.urls")),
    path("customerservice/", include("Customerservice.urls")),
    path("cart/", include("Shoppingcart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
