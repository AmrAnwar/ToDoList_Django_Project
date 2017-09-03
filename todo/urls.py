"""todo URL Configuration

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
import views
import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/(?P<username>[\w-]+)/$', views.ProfileView.as_view(), name="profile-detail"),
    url(r'^lists/(?P<pk>\d+)/$', views.ListDetailView.as_view(), name="lists-detail"),
    # url(r'lists/(?P<pk>\d+)/invite/(?P<code>/d+)/$', views., name="lists-invite"),
    url(r'^tasks/(?P<pk>\d+)/$', views.TaskDetailView.as_view(), name="tasks-detail"),
    url(r'^lists/$', views.ListsView.as_view(), name="lists-list"),
    url(r'^$', views.index, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
