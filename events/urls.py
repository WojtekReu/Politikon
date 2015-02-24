from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^fbobjects/event/(?P<event_id>\d+)/$', 'events.views.event_facebook_object_detail', name="event_facebook_object_detail"),
    url(r'^event/(?P<event_id>\d+)-[a-zA-Z0-9\-]+$', 'events.views.event_detail', name="event_detail"),
    url(r'^events/$', 'events.views.events', {'mode':'popular'}, name="events"),
    url(r'^events/(?P<mode>popular|latest|changed|finished)$', 'events.views.events', name="events"),

    url(r'^user/(?P<user_id>\d+)/portfolio$', 'events.views.user_portfolio'),
    url(r'^user/(?P<user_id>\d+)/transactions$', 'events.views.user_transactions'),

    url(r'^event/(?P<event_id>\d+)/transaction/create/$', 'events.views.create_transaction', name="create_transaction"),
)
