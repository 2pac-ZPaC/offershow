from django.conf.urls import patterns,url
from salary import views

urlpatterns = patterns("",
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^right/(?P<type>\d+)/$', views.right, name='right'),
    url(r'^offerrecord/', views.offerrecord, name='offerrecord'),
    url(r'^offerdetail/(?P<id>\d+)/$', views.offerdetail, name='offerdetail'),
    url(r'^offerlike/(?P<id>\d+)/$', views.offerlike, name='offerlike'),
    url(r'^offerdislike/(?P<id>\d+)/$', views.offerdislike, name='offerdislike'),
    # restful api
    url(r'^webapi/jobtotal/', views.jobtotal, name='jobtotal'),
    url(r'^webapi/jobrecord/', views.jobrecord, name='jobrecord'),
    url(r'^webapi/jobdetail/(?P<id>\d+)/$', views.jobdetail, name='jobdetail'),
    url(r'^webapi/joblike/(?P<id>\d+)/$', views.joblike, name='joblike'),
    url(r'^webapi/jobdislike/(?P<id>\d+)/$', views.jobdislike, name='jobdislike'),
)
