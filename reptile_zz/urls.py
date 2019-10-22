"""reptile_zz URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from show_reptile import views as show_reptile_views

urlpatterns = [
    url(r'^$',show_reptile_views.index,name='home'),
    url(r'^/ajax_dict/$',show_reptile_views.ajax_dict,name='ajax_dict'),
    url(r'^search/',show_reptile_views.search,name='search'),
    url(r'^infopages/',show_reptile_views.infopages,name='infopages'),
    url(r'show_one_article/',show_reptile_views.show_one_article,name='show_one_article'),
    url(r'^admin/', admin.site.urls),
]
