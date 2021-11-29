"""tempPjt URL Configuration

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
from students import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.get_main),
    path('admin', admin.site.urls),
    path('parameter', views.get_post),
    path('sensor', views.add_cur_wat),
    path('add', views.get_device),
    path('del', views.del_device),
    #del은 아직 삭제 구현x 그래서 전부 pass
    path('current', views.get_current),
    path('current2', views.get_current2),
    path('accumulate', views.get_accumulate),
    path('average', views.get_average),
    path('statistics', views.get_statistics)
    #path('Eproducts/', include('students.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
