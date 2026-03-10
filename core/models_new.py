from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="tracks")

    class Meta:
        ordering = ["title"]
        unique_together = ("title", "artist")

    def __str__(self):
        return f"{self.title} — {self.artist.name}"
