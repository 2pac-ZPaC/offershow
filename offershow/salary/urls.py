from django.conf.urls import patterns,url
from salary import views

urlpatterns = patterns("",
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^right/$', views.right),
    url(r'^right/(?P<type>\d+)/$', views.right, name='right'),
    url(r'^offerrecord/', views.offerrecord, name='offerrecord'),
    url(r'^offerdetail/(?P<id>\d+)/$', views.offerdetail, name='offerdetail'),
    url(r'^offerlike/(?P<id>\d+)/$', views.offerlike, name='offerlike'),
    url(r'^offerdislike/(?P<id>\d+)/$', views.offerdislike, name='offerdislike'),
    url(r'^offersearch/$', views.offersearch),
    url(r'^offersearch/(.+)/$', views.offersearch, name='offersearch'),

    # restful api
    url(r'^webapi/jobtotal/', views.jobtotal, name='jobtotal'),
    url(r'^webapi/jobrecord/', views.jobrecord, name='jobrecord'),
    url(r'^webapi/jobdetail/(?P<id>\d+)/$', views.jobdetail, name='jobdetail'),
    url(r'^webapi/joblike/(?P<id>\d+)/$', views.joblike, name='joblike'),
    url(r'^webapi/jobdislike/(?P<id>\d+)/$', views.jobdislike, name='jobdislike'),

    url(r'^webapi/jobcity/', views.jobcity, name='jobcity'),
    url(r'^webapi/jobcompany/', views.jobcompany, name='jobcompany'),
    url(r'^webapi/jobcount/', views.jobcount, name='jobcount'),
    url(r'^webapi/jobsearch/$', views.jobsearch),
    url(r'^webapi/jobsearch/(.+)/$', views.jobsearch, name='jobsearch'),
)
