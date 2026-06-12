"""clearance URL Configuration

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
from django.urls import include, path, re_path
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from clearance_app import api_views as cl_api_views
import clearance_app.views as cl_views
import management.views as management_views

from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
import django.contrib.auth.urls

from django.views.generic import TemplateView

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

router = routers.DefaultRouter()
router.register(r'mtlitemsset', cl_api_views.MtlItemViewset)
#router.register(r'wsitemsset', cl_api_views.WSItemViewset)

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('admin/logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path("", include("clearance_app.urls")),
    path("", include("management.urls")),
    path('admin/', admin.site.urls),
    re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('google7e89da1bf7749096.html', TemplateView.as_view(template_name='google7e89da1bf7749096.html'), name='google7e89da1bf7749096.html'),
    path('robots.txt', cl_views.robots_txt, name='robots_txt'),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    path('mtlitems/', cl_views.mtl_items_view, name='mtlitemsjson'),
    path('vesselitems/', cl_views.vessel_items_view, name='vesselitemsjson'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
