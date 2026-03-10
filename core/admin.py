from django.contrib import admin
from .models import AnnualWinner, ShowDetail, TrackListing
from core.models_new import Artist, Track

@admin.register(AnnualWinner)
class AnnualWinnerAdmin(admin.ModelAdmin):
    list_display = ('year', 'artist', 'album')

@admin.register(ShowDetail)
class ShowDetailAdmin(admin.ModelAdmin):
    list_display = ('show_id', 'show_date', 'album_of_the_week', 'year_in_britpop', 'notes', 'sotw_stat')

@admin.register(TrackListing)
class TrackListingAdmin(admin.ModelAdmin):
    list_display = ('track_id', 'show_id', 'play_order', 'artist', 'title', 'version', 'notes')