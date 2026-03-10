# Test comment for GIT

from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.db.models import Q, Count, Max
from .models import ShowDetail, TrackListing, AnnualWinner
from django.http import JsonResponse
from .models_new import Artist, Track
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import TrackListingForm
from decimal import Decimal

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


@login_required
def home(request):

    # --- Basic Stats ---
    total_tracks = TrackListing.objects.count()
    total_distinct_tracks = (
        TrackListing.objects
        .values('artist', 'title')
        .distinct()
        .count()
    )
    total_artists = TrackListing.objects.values('artist').distinct().count()
    total_shows = TrackListing.objects.values('show__show_date').distinct().count()
    busiest_show = (TrackListing.objects
    .values("show_id", "show__show_date")
    .annotate(track_count=Count("track_id"))
    .order_by("-track_count")
    .first())


    # --- Top 10 Most Played Artists ---
    top_artists = (
        TrackListing.objects
        .values('artist')
        .annotate(play_count=Count('artist'))
        .order_by('-play_count')[:10]
    )

    # --- Top 10 Most Played Tracks ---
    top_tracks = (
        TrackListing.objects
        .values('artist', 'title')
        .annotate(play_count=Count('track_id'))
        .order_by('-play_count')[:10]
    )

    # --- Top Artists by Number of Distinct Tracks ---
    top_artists_by_distinct_tracks = (
    TrackListing.objects
        .values('artist')
        .annotate(distinct_track_count=Count('title', distinct=True))
        .order_by('-distinct_track_count')[:10]
)


    # --- Top 10 Most Requested Artists (Notes = "LC") ---
    top_requested_artists = (
        TrackListing.objects
        .filter(notes="LC")
        .values('artist')
        .annotate(request_count=Count('artist'))
        .order_by('-request_count')[:10]
    )

    # --- Top 10 Most Requested Tracks (Notes = "LC") ---
    top_requested_tracks = (
        TrackListing.objects
        .filter(notes="LC")
        .values("artist", "title")
        .annotate(request_count=Count("track_id"))
        .order_by("-request_count")[:10]
    )

    context = {
        "total_tracks": total_tracks,
        "total_distinct_tracks": total_distinct_tracks,
        "total_artists": total_artists,
        "total_shows": total_shows,
        "top_artists": top_artists,
        "top_tracks": top_tracks,
        "top_requested_artists": top_requested_artists,
        "top_requested_tracks": top_requested_tracks,
        "busiest_show": busiest_show,
        "top_artists_by_distinct_tracks": top_artists_by_distinct_tracks,
    }

    return render(request, 'home.html', context)


class ShowDetailForm(ModelForm):
    class Meta:
        model = ShowDetail
        fields = '__all__'
        widgets = {
            'show_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'show_date': forms.DateInput(attrs={'type': 'date'}),

# Larger text boxes
            'album_of_the_week': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
            'notes': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
            'sotw_stat': forms.Textarea(attrs={'rows': 1, 'cols': 60}),

        }

@login_required
def search_artist(request):
    query = request.GET.get("artist", "").strip()
    results = []
    track_summary = []

    if query:
        # Main search results
        results = TrackListing.objects.filter(artist__icontains=query)

        # Distinct tracks + play count
        track_summary = (
            TrackListing.objects
            .filter(artist__icontains=query)
            .values("title")
            .annotate(play_count=Count("title"))
            .order_by("-play_count")
        )

    return render(request, "search_artist.html", {
        "query": query,
        "results": results,
        "track_summary": track_summary,
    })


@login_required
def search_track(request):
    query = request.GET.get("track", "")
    track_results = []
    tracklisting_results = []

    # Autocomplete search results
    if query:
        track_results = Track.objects.filter(title__icontains=query)

        # If the query exactly matches a track title, fetch all matching rows
        if Track.objects.filter(title=query).exists():
            tracklisting_results = TrackListing.objects.filter(title=query).order_by("show_id", "play_order")

    return render(request, "search_track.html", {
        "query": query,
        "track_results": track_results,
        "tracklisting_results": tracklisting_results,
    })


@login_required
def autocomplete_artist(request):
    term = request.GET.get("term", "").strip()

    artists = (
        TrackListing.objects
        .filter(artist__icontains=term)
        .values_list("artist", flat=True)
        .distinct()
        .order_by("artist")[:10]
    )

    return JsonResponse(list(artists), safe=False)



@login_required
def autocomplete_track(request):
    term = request.GET.get("term", "").strip()
    artist = request.GET.get("artist", "").strip()

    qs = TrackListing.objects.all()

    # Filter by selected artist
    if artist:
        qs = qs.filter(artist__iexact=artist)

    # Filter by track title search term
    if term:
        qs = qs.filter(title__icontains=term)

    tracks = (
        qs.values_list("title", flat=True)
        .distinct()
        .order_by("title")[:10]
    )

    return JsonResponse(list(tracks), safe=False)


@login_required
def add_tracklisting(request):
    # List of existing tracks for the dropdown
    tracks = TrackListing.objects.order_by("-track_id")

    # EDIT MODE
    edit_id = request.GET.get("edit")
    if edit_id:
        instance = TrackListing.objects.get(track_id=edit_id)

        if request.method == "POST":
            form = TrackListingForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("add_tracklisting")
        else:
            form = TrackListingForm(instance=instance)

        return render(request, "add_tracklisting.html", {
            "form": form,
            "tracks": tracks,
            "edit_mode": True,
            "edit_id": edit_id,
        })

    # ADD MODE
    show_id = request.GET.get("show_id")

    # Default to highest show_id if none provided
    if not show_id:
        latest_show = ShowDetail.objects.aggregate(max_id=Max("show_id"))["max_id"]
        if latest_show:
            show_id = str(latest_show)

    if request.method == 'POST':
        form = TrackListingForm(request.POST)
        if form.is_valid():
            saved = form.save()
            return redirect(f"{reverse('add_tracklisting')}?show_id={saved.show_id}")
    else:
        # Determine next global track_id
        max_track_id = TrackListing.objects.aggregate(max_id=Max('track_id'))['max_id']
        next_track_id = 1 if max_track_id is None else max_track_id + 1

        initial_data = {
            'track_id': next_track_id,
        }

        if show_id:
            # Correct field name is "show"
            initial_data['show'] = show_id

            # Correct field name is "play_order"
            next_play_order = TrackListing.objects.filter(show_id=show_id).count() + 1
            initial_data['play_order'] = next_play_order

        form = TrackListingForm(initial=initial_data)

        if show_id:
            form.fields['show'].disabled = True

    return render(request, 'add_tracklisting.html', {
        'form': form,
        'tracks': tracks,
        'edit_mode': False,
    })


@login_required
def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = TrackListing.objects.filter(
            Q(artist__icontains=query) |
            Q(title__icontains=query)
        )

    return render(request, 'search.html', {
        'query': query,
        'results': results
    })


@login_required
def stats(request):
    total_shows = ShowDetail.objects.count()
    total_tracks = TrackListing.objects.count()
    total_distinct_tracks = (
    TrackListing.objects
    .values('artist', 'title')
    .distinct()
    .count()
    )
    total_winners = AnnualWinner.objects.count()

    top_artists = (
        TrackListing.objects
        .values('artist')
        .annotate(count=Count('artist'))
        .order_by('-count')[:10]
    )

    return render(request, 'stats.html', {
        'total_shows': total_shows,
        'total_tracks': total_tracks,
        'total_distinct_tracks': total_distinct_tracks,
        'total_winners': total_winners,
        'top_artists': top_artists,
    })



@login_required
def add_show(request):
    shows = ShowDetail.objects.order_by("-show_id")

    edit_id = request.GET.get("edit")
    instance = None
    edit_mode = False

    if edit_id:
        edit_mode = True
        instance = ShowDetail.objects.get(show_id=edit_id)

    if request.method == "POST":
        form = ShowDetailForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("add_show")  # reload cleanly
    else:
        form = ShowDetailForm(instance=instance)

        if not edit_mode:
            max_id = ShowDetail.objects.aggregate(max_id=Max('show_id'))['max_id']
            next_id = 1 if max_id is None else int(max_id) + 1
            form.initial['show_id'] = next_id

    return render(request, "add_show.html", {
        "form": form,
        "shows": shows,
        "edit_mode": edit_mode,
    })


@login_required
def track_detail(request, title):
    plays = TrackListing.objects.filter(title=title).order_by("-show_id")

    return render(request, "track_detail.html", {
        "title": title,
        "plays": plays,
    })


@login_required
def next_play_order(request):
    show_id = request.GET.get("show_id")

    if not show_id:
        return JsonResponse({"next": 1})

    last_order = (
        TrackListing.objects
        .filter(show_id=show_id)
        .aggregate(max_order=Max("play_order"))
        ["max_order"]
    )

    next_order = 1 if last_order is None else last_order + 1

    return JsonResponse({"next": next_order})

@login_required
def stotw_list(request):
    stotw_tracks = (
        TrackListing.objects
        .filter(notes="STotW")
        .select_related("show")
        .order_by("-show__show_date", "play_order")
    )

    return render(request, "stotw_list.html", {
        "tracks": stotw_tracks
    })