from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrackListing, Artist, Track

@receiver(post_save, sender=TrackListing)
def sync_artist_track(sender, instance, created, **kwargs):
    """
    Ensures Artist, Track, and canonical_track stay in sync whenever
    a new TrackListing row is created.
    """

    # Only run on creation
    if not created:
        return

    # Skip if no artist/title entered
    if not instance.artist or not instance.title:
        return

    artist_name = instance.artist.strip()
    track_title = instance.title.strip()

    # 1. Ensure Artist exists
    artist_obj, _ = Artist.objects.get_or_create(name=artist_name)

    # 2. Ensure Track exists
    track_obj, _ = Track.objects.get_or_create(
        title=track_title,
        artist=artist_obj
    )

    # 3. Assign canonical_track if missing
    if instance.canonical_track is None:
        instance.canonical_track = track_obj
        instance.save(update_fields=["canonical_track"])