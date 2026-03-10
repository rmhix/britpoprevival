from django.core.management.base import BaseCommand
from core.models import TrackListing
from core.models_new import Artist, Track

class Command(BaseCommand):
    help = "Import unique artists and tracks from TrackListing into Artist and Track tables"

    def handle(self, *args, **kwargs):
        artist_count = 0
        track_count = 0

        for row in TrackListing.objects.all():
            if not row.artist or not row.title:
                continue

            artist_obj, created_artist = Artist.objects.get_or_create(name=row.artist.strip())
            if created_artist:
                artist_count += 1

            track_obj, created_track = Track.objects.get_or_create(
                title=row.title.strip(),
                artist=artist_obj
            )
            if created_track:
                track_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete: {artist_count} new artists, {track_count} new tracks."
        ))