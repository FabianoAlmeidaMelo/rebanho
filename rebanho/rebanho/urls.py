"""rebanho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import (
            logout,
            login,
        )
from rebanho.core.forms import AuthenticationForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('rebanho.api.urls')),
    url(r'^', include('rebanho.core.urls')),
    url(r'^', include('rebanho.propriedades.urls')),
    # Login Logout
    url(r'^logout/$', logout, {"next_page": None}, name="logout"),
    url(r'^logout/(?P<next_page>.*)/$', logout, name='auth_logout_next'),
    url(r'^login/$', login,
        {"template_name": 'login.html', "authentication_form": AuthenticationForm,},
        name="login"),
]

