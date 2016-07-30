from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^start_game/$', views.start_game, name='start_game'),
	url(r'^play_game/$', views.play_game, name='play_game'),
	url(r'^enter_room/$', views.enter_room, name='enter_room'),
	url(r'^create_room/$', views.create_room, name='create_room'),
	url(r'^finish_game/(?P<room_id>\d+)/$', views.finish_game, name='finish_game'),
	url(r'^about_game/$', views.about_game, name='about_game'),
]