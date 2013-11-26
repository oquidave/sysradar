from django.conf.urls import patterns, include, url
from monitor import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sysradar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #http://127.0.0.1:8000/check_serverip/?ip=127.0.0.1
    url(r'^check_serverip/$', views.check_serverip),
    #http://127.0.0.1:8000/check_service/?port=22
    url(r'^check_service/$', views.check_service),
    #http://127.0.0.1:8000/add_box/?ip=127.0.0.1&box_name=localhost
    url(r'^add_box/$', views.add_box),
    #get_boxes
    url(r'^get_boxes/$', views.get_boxes),
    url(r'^get_box_services/$', views.get_box_services),
    #check_box_services
    url(r'^box_services/$', views.check_box_services),
    #service_control
    url(r'^service_control/$', views.service_control),
     
     
    
)
