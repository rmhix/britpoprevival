from django.urls import path
from . import views
from core.health import health
from .views import backfill_canonical

urlpatterns = [
    path("health/", health),
    path('', views.home, name='home'),
    path('add-show/', views.add_show, name='add_show'),
    path('search/', views.search, name='search'),
    path("search/artist/", views.search_artist, name="search_artist"),
    path("search/track/", views.search_track, name="search_track"),
    path("autocomplete/artist/", views.autocomplete_artist,   name="autocomplete_artist"),
    path("autocomplete/track/", views.autocomplete_track, name="autocomplete_track"),
    path("track/<int:id>/", views.track_detail, name="track_detail"),
    path("add-tracklisting/", views.add_tracklisting, name="add_tracklisting"),
    path("ajax/next-play-order/", views.next_play_order, name="next_play_order"),
    path("stotw/", views.stotw_list, name="stotw_list"),
    path("api/latest-tracklist/", views.latest_tracklist, name="latest_tracklist"),
    path("backfill/", backfill_canonical),

]
