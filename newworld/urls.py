"""newworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

import newworld.views
import joins.views

urlpatterns = [
	url(r'^$', joins.views.list, name='list'),
    # url(r'^list/', joins.views.list, name='list'),
    url(r'^update/', joins.views.updatedb, name='updatedb'),
    url(r'^updatedup/', joins.views.updatedup, name='updatedup'),
    url(r'^(?P<page_id>[0-9]{18})/editinfo/', joins.views.editinfo, name='editinfo'),
    # url(r'^(?P<page_id>[0-9]{18})/deleteapt/', joins.views.deleteapt, name='editinfo'),
    url(r'^(?P<page_id>[0-9]{18})/setscam/', joins.views.setscam, name='setscam'),
    url(r'^(?P<page_id>[0-9]{18})/setemailsent/', joins.views.setemailsent, name='setemailsent'),
    url(r'^(?P<page_id>[0-9]{18})/setbroker/', joins.views.setbroker, name='setbroker'),
    url(r'^(?P<page_id>[0-9]{18})/setscam2/', joins.views.setscam2, name='setscam'),
    url(r'^(?P<page_id>[0-9]{18})/setemailsent2/', joins.views.setemailsent2, name='setemailsent'),
    url(r'^(?P<page_id>[0-9]{18})/setbroker2/', joins.views.setbroker2, name='setbroker2'),
    url(r'^search/', joins.views.search, name='search'),
    url(r'^updateneighbors/', joins.views.updateneighbors, name='neighbors'),
    url(r'^updateshortneighborhoodid/', joins.views.updateshortneighborhoodid, name='hashids'),
    url(r'^updateparentneighborhood/', joins.views.updateparentneighborhood, name='parentneighb'),
    url(r'^sendrequesttoanni.*/', joins.views.sendrequesttoanni, name='sendrequest'),
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<page_id>[0-9]{18})/$', joins.views.apt),
    url(r'^find/', joins.views.find, name='find'),
]
