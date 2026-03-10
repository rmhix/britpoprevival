from django import forms
from django.forms import ModelForm
from .models import TrackListing, ShowDetail

class TrackListingForm(ModelForm):
    class Meta:
        model = TrackListing
        fields = [
            "track_id",
            "show",
            "play_order",
            "artist",
            "title",
            "version",
            "notes",
        ]
        widgets = {
            "track_id": forms.NumberInput(attrs={"readonly": "readonly"}),
            "notes": forms.Textarea(attrs={"rows": 1}),
        }

class ShowDetailForm(forms.ModelForm):
    class Meta:
        model = ShowDetail
        fields = [
            "show_id",
            "show_date",
            "album_of_the_week",
            "year_in_britpop",
            "notes",
            "sotw_stat",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force initial values from instance for unmanaged models
        if self.instance and self.instance.pk:
            self.fields["show_id"].initial = self.instance.show_id
            self.fields["show_date"].initial = self.instance.show_date
            self.fields["album_of_the_week"].initial = self.instance.album_of_the_week
            self.fields["year_in_britpop"].initial = self.instance.year_in_britpop
            self.fields["notes"].initial = self.instance.notes
            self.fields["sotw_stat"].initial = self.instance.sotw_stat

class ArtistSearchForm(forms.Form):
    artist = forms.CharField(label="Artist", required=False)

class TrackSearchForm(forms.Form):
    track = forms.CharField(label="Track", required=False)