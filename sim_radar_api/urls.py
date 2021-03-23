"""sim_radar_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.static import serve
from django.conf import settings
from rest_framework.documentation import include_docs_urls

# xadmin的依赖
import xadmin
xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('admin/', admin.site.urls),

    path('xadmin/', xadmin.site.urls),

    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path('course/', include('course.urls')),
    path('radar/', include('radar.urls')),

    # 打开 media 文件夹
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    # 接口文档
    path('docs/', include_docs_urls(title='接口文档'))
]
