"""election URL Configuration

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

from app1.views import add_candidates_view, add_candidates_code, homepage_view, start_category_voting, start_voting, get_results


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name="home"),
    path('add_C', add_candidates_view, name="add_C"),
    path('start_vote/', start_voting, name="start_vote"),
    path('add_code', add_candidates_code, name="add_code"),
    path('add_vote/', start_category_voting, name='add_vote'),
    path('results/', get_results, name='results'),
]
