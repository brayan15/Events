from django.conf.urls import url


from events.events.views import HomeView , CreateEvent

#app_name = 'events'

urlpatterns = [
   url(r'^event/new/$',CreateEvent.as_view(),name='create_event'),
]
