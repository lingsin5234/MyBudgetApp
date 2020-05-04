"""appsetup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings

from budget import views as budget_views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^display/', budget_views.show_data),
    re_path(r'^upload/(?P<upload_type>[\w_]+)/$', budget_views.upload_data),
    re_path(r'^upload_done/(?P<upload_type>[\w_]+)/$', budget_views.upload_done),
    # re_path(r'^dashboard/$', budget_views.show_d3),
    re_path(r'^dashboard/$', budget_views.show_dashboard),
    re_path(r'^show_cat/(?P<cat_type>[\w_]+)/$', budget_views.show_category),
    re_path(r'^project/$', budget_views.project_markdown),
    re_path(r'^$', budget_views.project_markdown),


    # plotly dash
    re_path(r'^dashboard2/$', budget_views.show_plotly_dash),
    path('django_plotly_dash/', include('django_plotly_dash.urls'))
]
