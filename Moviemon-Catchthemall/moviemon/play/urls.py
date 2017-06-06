from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.title_screen, name="title_screen"),
    url(r'^worldmap/?$', views.worldmap, name="worldmap"),
    url(r'^battle/?$', views.battle, name="battle"),
    url(r'^battle/(?P<moviemon_id>[a-zA-Z0-9 _:.\'!-]+)/?$', views.battle_moviemon, name='battle_moviemon'),
    url(r'^moviedex/?$', views.moviedex, name="moviedex"),
    url(r'^moviedex/(?P<moviemon_id>tt[0-9]+)/?$', views.moviedex_moviemon, name='moviedex_moviemon'),
    url(r'^options/?$', views.options, name="options"),
    url(r'^options/save_game/?$', views.options_save_game, name="options_save_game"),
    url(r'^options/load_game/?$', views.options_load_game, name="options_load_game"),
]
