from django.conf.urls import url


from events.events.views import HomeView , CreateEvent, DetailEvent

#app_name = 'events'

urlpatterns = [
   url(r'^event/new/$',CreateEvent.as_view(),name='create_event'),
   url(r'^detail/(?P<pk>[0-9a-f-]+)/$',
        DetailEvent.as_view(), name='detail_event'),
]
