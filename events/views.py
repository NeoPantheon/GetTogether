import datetime

from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import simplejson
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from .forms import EventCommentForm
from .models.events import Attendee, Event, EventComment, Place, PlaceSerializer
from .models.locale import (
    SPR,
    City,
    CitySerializer,
    Country,
    CountrySerializer,
    SPRSerializer,
)
from .models.profiles import (
    Member,
    Organization,
    Sponsor,
    SponsorSerializer,
    Team,
    TeamSerializer,
    UserProfile,
)
from .models.search import Searchable, SearchableSerializer
from .utils import verify_csrf


# Create your views here.
def searchable_list(request, *args, **kwargs):
    searchables = Searchable.objects.exclude(location_name="")
    serializer = SearchableSerializer(searchables, many=True)
    return JsonResponse(serializer.data, safe=False)


def events_list(request, *args, **kwargs):
    events = Event.objects.all()
    context = {"events_list": events}
    return render(request, "events/event_list.html", context)


def upcoming_events(request):
    searchables = (
        Searchable.objects.exclude(location_name="")
        .filter(end_time__gte=timezone.now())
        .order_by("start_time")
    )
    unique_events = dict()
    for event in searchables:
        if event.group_name not in unique_events:
            unique_events[event.group_name] = event
    serializer = SearchableSerializer(unique_events.values(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def teams_list(request):
    serializer = TeamSerializer(Team.public_objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def org_member_list(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    serializer = TeamSerializer(org.teams.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def places_list(request, *args, **kwargs):
    places = Place.objects.all()
    if "q" in request.GET:
        match = request.GET.get("q", "")
        places = Place.objects.filter(name__icontains=match)
    else:
        places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def country_list(request, *args, **kwargs):
    if "q" in request.GET:
        match = request.GET.get("q", "")
        countries = Country.objects.filter(name__icontains=match)[:20]
    else:
        countries = Country.objects.all()[:20]
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def spr_list(request, *args, **kwargs):
    if "q" in request.GET:
        match = request.GET.get("q", "")
        sprs = SPR.objects.filter(name__icontains=match)[:20]
    else:
        sprs = SPR.objects.all()[:20]
    if "country" in request.GET and request.GET.get("country") is not "":
        sprs = sprs.filter(country=request.GET.get("country"))

    serializer = SPRSerializer(sprs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def city_list(request, *args, **kwargs):
    if "q" in request.GET:
        match = request.GET.get("q", "")
        cities = City.objects.filter(name__icontains=match).order_by("-population")
    else:
        cities = City.objects.all()

    if "spr" in request.GET and request.GET.get("spr") is not "":
        cities = cities.filter(spr=request.GET.get("spr"))

    serializer = CitySerializer(cities[:50], many=True)
    return Response(serializer.data)


@api_view(["GET"])
def find_city(request):
    cities = City.objects.all()
    if "city" in request.GET:
        cities = cities.filter(name=request.GET.get("city"))
    if "spr" in request.GET:
        cities = cities.filter(spr__name=request.GET.get("spr"))
    if "country" in request.GET:
        cities = cities.filter(spr__country__name=request.GET.get("country"))
    try:
        city = cities[0]
        serializer = CitySerializer(city)
        return Response(serializer.data)
    except:
        return Response({})


@api_view(["GET"])
def sponsor_list(request):
    if "q" in request.GET:
        match = request.GET.get("q", "")
        sponsors = Sponsor.objects.filter(name__icontains=match)
    else:
        sponsors = Sponsor.objects.all()

    serializer = SponsorSerializer(sponsors[:50], many=True)
    return Response(serializer.data)


@verify_csrf(token_key="csrftoken")
def join_team(request, team_id):

    team = Team.objects.get(id=team_id)
    if team.access == Team.PRIVATE:
        raise Http404()
    if request.user.is_anonymous:
        messages.add_message(
            request,
            messages.WARNING,
            message=_("You must be logged in to join a team."),
        )
        return redirect("show-team", team_id=team_id)
    if request.user.profile in team.members.all():
        messages.add_message(
            request, messages.INFO, message=_("You are already a member of this team.")
        )
        return redirect("show-team", team_id=team_id)
    new_member = Member.objects.create(
        team=team, user=request.user.profile, role=Member.NORMAL
    )
    messages.add_message(request, messages.SUCCESS, message=_("Welcome to the team!"))
    return redirect("show-team", team_id=team_id)


@verify_csrf(token_key="csrftoken")
def leave_team(request, team_id):
    if request.user.is_anonymous:
        messages.add_message(
            request,
            messages.WARNING,
            message=_("You must be logged in to leave a team."),
        )
        return redirect("show-team", team_id=team_id)
    team = Team.objects.get(id=team_id)
    if request.user.profile not in team.members.all():
        messages.add_message(
            request, messages.INFO, message=_("You are not a member of this team.")
        )
        return redirect("show-team", team_id=team_id)
    Member.objects.filter(team=team, user=request.user.profile).delete()
    messages.add_message(
        request, messages.SUCCESS, message=_("You are no longer on this team.")
    )
    return redirect("show-team", team_id=team_id)
