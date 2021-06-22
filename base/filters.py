from django.db.models.query import QuerySet
from django.forms import widgets
import django_filters
from django_filters import filters
from .models import Practice, Piece, User, Instrument
from django.forms.widgets import DateTimeInput, Select, SplitDateTimeWidget, SelectDateWidget, TextInput
from durationwidget.widgets import TimeDurationWidget

def instruments(request):
    if request is None:
        return Instrument.objects.none()
    return Instrument.objects.filter(user=request.user)

def pieces(request):
    if request is None:
        return Piece.objects.none()
    return Piece.objects.filter(user=request.user)

class PracticeFilter(django_filters.FilterSet):
    
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte', label='Date from', widget=SelectDateWidget(years=range(2015, 2030), attrs={'class': 'filter-field session-start-date'}))
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte', label='Date till', widget=SelectDateWidget(years=range(2015, 2030), attrs={'class': 'filter-field session-end-date'}))
    min_duration = filters.DurationFilter(field_name='duration', lookup_expr='gte', label='Duration from', widget=TimeDurationWidget(show_days=False, show_hours=True, show_minutes=True, show_seconds=False, attrs={'class': 'filter-field session-duration-min'}))
    max_duration = filters.DurationFilter(field_name='duration', lookup_expr='lte', label='Duration till', widget=TimeDurationWidget(show_days=False, show_hours=True, show_minutes=True, show_seconds=False, attrs={'class': 'filter-field session-duration-max'}))
    piece = filters.ModelChoiceFilter(queryset=pieces, widget=Select(attrs={'class': 'filter-field session-piece'}))
    instrument = filters.ModelChoiceFilter(queryset=instruments, widget=Select(attrs={'class': 'filter-field session-instrument'}))
    notes = filters.CharFilter(lookup_expr='icontains', label='Notes', widget=TextInput(attrs={'class': 'filter-field session-notes'}))


    class Meta:
        model = Practice
        fields = ('instrument', 'piece', 'notes')

class PieceFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Name:', widget=TextInput(attrs={'class': 'filter-field piece-name'}))
    artist = filters.CharFilter(lookup_expr='icontains', label='Artist', widget=TextInput(attrs={'class': 'filter-field piece-artist'}))
    album = filters.CharFilter(lookup_expr='icontains', label='Album', widget=TextInput(attrs={'class': 'filter-field piece-album'}))
    notes = filters.CharFilter(lookup_expr='icontains', label='Notes', widget=TextInput(attrs={'class': 'filter-field piece-notes'}))

    class Meta:
        model = Piece
        fields = ('name', 'artist', 'album', 'notes')


class InstrumentFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Name:', widget=TextInput(attrs={'class': 'filter-field instrument-name'}))
    notes = filters.CharFilter(lookup_expr='icontains', label='Notes', widget=TextInput(attrs={'class': 'filter-field instrument-notes'}))

    class Meta:
        model = Piece
        fields = ('name', 'notes')
