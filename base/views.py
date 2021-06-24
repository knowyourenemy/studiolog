import datetime

from django.core.exceptions import ValidationError

from base.models import Piece, Practice, Instrument
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django import forms
from django.forms.widgets import DateTimeInput, Select, SplitDateTimeWidget, SelectDateWidget, TextInput, Textarea
from durationwidget.widgets import TimeDurationWidget
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .filters import InstrumentFilter, PieceFilter, PracticeFilter
from django.db.models import Max, Avg, Sum, Count

# Create your views here.
class InfoView(TemplateView):
    template_name = 'base/info.html'
    


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('practice list')

class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('practice list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('practice list')
        return super(RegisterView, self).get(*args, **kwargs)





class PracticeList(LoginRequiredMixin, ListView):
    model = Practice
    context_object_name = 'sessions'
    ordering = ['-date']
    login_url = reverse_lazy('info')

    def current_streak(self):
        total_streak = 0
        current_streak = 0
        today = datetime.date.today()
        compareDate = today + datetime.timedelta(1) # Tomorrow

        # Using list() here pulls all the entries from the DB at once
        # Gets all entry dates for this journal and whose dates are <= today
        entry_dates = list(Practice.objects.values("date").filter(user=self.request.user, date__lte = today).order_by("-date"))

        for date in entry_dates:
            # Get the difference btw the dates
            delta = compareDate - date.get("date")

            if delta.days == 1: # Keep the streak going!
                current_streak += 1
            elif delta.days == 0: # Don't bother increasing the day if there's multiple ones on the same day
                pass
            else: # Awwww...
                break # The current streak is done, exit the loop

            compareDate = date.get("date")

        if current_streak > total_streak:
            total_streak = current_streak

        return total_streak
  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = context['sessions'].filter(user=self.request.user)
        context['filter'] = PracticeFilter(self.request.GET, queryset=self.get_queryset().filter(user=self.request.user), request=self.request)
        context['streak'] = self.current_streak()
        context['longest_session'] = context['sessions'].aggregate(Max('duration')).get('duration__max')
        context['avg_session'] = context['sessions'].aggregate(Avg('duration')).get('duration__avg')
        context['sum_session'] = context['sessions'].aggregate(Sum('duration')).get('duration__sum')
        return context



class PracticeDetail(LoginRequiredMixin, DetailView):
    model = Practice
    context_object_name = 'session'
    login_url = reverse_lazy('info')

class PracticeCreate(LoginRequiredMixin, CreateView):
    model = Practice
    fields = ['date', 'duration', 'instrument', 'piece', 'notes']
    success_url = reverse_lazy('practice list')
    date_range = 1
    this_year = datetime.datetime.now().year
    login_url = reverse_lazy('info')

    def validate_duration(self, value):
        if value < datetime.timedelta(days=0, seconds=0):
            raise ValidationError(
                "duration is too low"
            )
        if value > datetime.timedelta(days = 0, hours=23, minutes=59, seconds=59):
            raise ValidationError(
                "duration is too high"
            )
        

    def get_form(self):
        form = super(PracticeCreate, self).get_form()
        form.fields['date'].widget = SelectDateWidget(years=range(self.this_year - self.date_range, self.this_year + self.date_range + 1), attrs={'class': 'create-field session-date'})
        form.fields['duration'].widget = TimeDurationWidget(show_days=False, show_hours=True, show_minutes=True, show_seconds=False, attrs={'class': 'create-field session-duration'})
        form.fields['instrument'].widget = Select(attrs={'class': 'create-field session-instrument'})
        form.fields['piece'].widget = Select(attrs={'class': 'create-field session-piece'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field session-notes'})
        form.fields['piece'].queryset = Piece.objects.filter(user=self.request.user)
        form.fields['instrument'].queryset = Instrument.objects.filter(user=self.request.user)
        form.fields['date'].initial = datetime.datetime.now()
        form.fields['duration'].validators=[self.validate_duration]
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PracticeCreate, self).form_valid(form)

class PracticeUpdate(LoginRequiredMixin, UpdateView):
    model = Practice
    fields = ['date', 'duration', 'instrument', 'piece', 'notes']
    success_url = reverse_lazy('practice list')
    date_range = 1
    this_year = datetime.datetime.now().year
    login_url = reverse_lazy('info')

    def validate_duration(self, value):
        if value < datetime.timedelta(days=0, seconds=0):
            raise ValidationError(
                "duration is too low"
            )
        if value > datetime.timedelta(days = 0, hours=23, minutes=59, seconds=59):
            raise ValidationError(
                "duration is too high"
            )

    def get_form(self):
        form = super(PracticeUpdate, self).get_form()
        form.fields['date'].widget = SelectDateWidget(years=range(self.this_year - self.date_range, self.this_year + self.date_range + 1), attrs={'class': 'create-field session-date'})
        form.fields['duration'].widget = TimeDurationWidget(show_days=False, show_hours=True, show_minutes=True, show_seconds=False, attrs={'class': 'create-field session-duration'})
        form.fields['instrument'].widget = Select(attrs={'class': 'create-field session-instrument'})
        form.fields['piece'].widget = Select(attrs={'class': 'create-field session-piece'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field session-notes'})
        form.fields['piece'].queryset = Piece.objects.filter(user=self.request.user)
        form.fields['instrument'].queryset = Instrument.objects.filter(user=self.request.user)
        form.fields['duration'].validators=[self.validate_duration]
        
        return form

class PracticeDelete(LoginRequiredMixin, DeleteView):
    model = Practice
    context_object_name = 'session'
    success_url = reverse_lazy('practice list')
    login_url = reverse_lazy('info')

class InstrumentList(LoginRequiredMixin, ListView):
    model = Instrument
    context_object_name = 'instruments'
    login_url = reverse_lazy('info')

    def get_most_practiced(self, instruments):
        most_practiced_name = ""
        most_practiced_hours = datetime.timedelta(days=0, seconds=0)
        for instrument in instruments:
            current_sum = instrument.sessions.all().aggregate(Sum('duration')).get('duration__sum')
            if current_sum is None:
                continue
            print(current_sum)
            if current_sum > most_practiced_hours:
                most_practiced_hours = current_sum
                most_practiced_name = instrument.name

        return most_practiced_name, most_practiced_hours


    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instruments'] = context['instruments'].filter(user=self.request.user)
        context['filter'] = InstrumentFilter(self.request.GET, queryset=self.get_queryset().filter(user=self.request.user), request=self.request)
        context['most_practiced_name'], context['most_practiced_hours'] = self.get_most_practiced(context['instruments'])
        context['total_instruments'] = context['instruments'].aggregate(Count('name')).get('name__count')
        return context

class InstrumentDetail(LoginRequiredMixin, DetailView):
    model = Instrument
    context_object_name = 'instrument'
    login_url = reverse_lazy('info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_session'] = context['instrument'].sessions.all().aggregate(Avg('duration')).get('duration__avg')
        context['sum_session'] = context['instrument'].sessions.all().aggregate(Sum('duration')).get('duration__sum')
        return context

class InstrumentCreate(LoginRequiredMixin, CreateView):
    model = Instrument
    fields = ['name', 'notes']
    success_url = reverse_lazy('instrument list')
    login_url = reverse_lazy('info')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(InstrumentCreate, self).form_valid(form)

    def get_form(self):
        form = super(InstrumentCreate, self).get_form()
        form.fields['name'].widget = TextInput(attrs={'class': 'create-field instrument-name'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field instrument-notes'})
        return form


class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    fields = ['name', 'notes']
    success_url = reverse_lazy('instrument list')
    login_url = reverse_lazy('info')

    def get_form(self):
        form = super(InstrumentUpdate, self).get_form()
        form.fields['name'].widget = TextInput(attrs={'class': 'create-field instrument-name'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field instrument-notes'})
        return form


class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    context_object_name = 'instrument'
    success_url = reverse_lazy('instrument list')
    login_url = reverse_lazy('info')

class PieceList(LoginRequiredMixin, ListView):
    model = Piece
    context_object_name = 'pieces'
    login_url = reverse_lazy('info')

    def get_most_practiced(self, pieces):
        most_practiced_name = ""
        most_practiced_hours = datetime.timedelta(days=0, seconds=0)
        for piece in pieces:
            current_sum = piece.sessions.all().aggregate(Sum('duration')).get('duration__sum')
            if current_sum is None:
                continue
            print(current_sum)
            if current_sum > most_practiced_hours:
                most_practiced_hours = current_sum
                most_practiced_name = piece.name

        return most_practiced_name, most_practiced_hours


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pieces'] = context['pieces'].filter(user=self.request.user)
        context['filter'] = PieceFilter(self.request.GET, queryset=self.get_queryset().filter(user=self.request.user), request=self.request)
        context['most_practiced_name'], context['most_practiced_hours'] = self.get_most_practiced(context['pieces'])
        context['total_pieces'] = context['pieces'].aggregate(Count('name')).get('name__count')
        return context

class PieceDetail(LoginRequiredMixin, DetailView):
    model = Piece
    context_object_name = 'piece'
    login_url = reverse_lazy('info')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_session'] = context['piece'].sessions.all().aggregate(Avg('duration')).get('duration__avg')
        context['sum_session'] = context['piece'].sessions.all().aggregate(Sum('duration')).get('duration__sum')
        return context

    

class PieceCreate(LoginRequiredMixin, CreateView):
    model = Piece
    fields = ['name', 'artist', 'album', 'notes']
    success_url = reverse_lazy('piece list')
    login_url = reverse_lazy('info')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PieceCreate, self).form_valid(form)
    
    def get_form(self):
        form = super(PieceCreate, self).get_form()
        form.fields['name'].widget = TextInput(attrs={'class': 'create-field piece-name'})
        form.fields['artist'].widget = TextInput(attrs={'class': 'create-field piece-artist'})
        form.fields['album'].widget = TextInput(attrs={'class': 'create-field piece-album'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field piece-notes'})
        return form

class PieceUpdate(LoginRequiredMixin, UpdateView):
    model = Piece
    fields = ['name', 'artist', 'album', 'notes']
    success_url = reverse_lazy('piece list')
    login_url = reverse_lazy('info')

    def get_form(self):
        form = super(PieceUpdate, self).get_form()
        form.fields['name'].widget = TextInput(attrs={'class': 'create-field piece-name'})
        form.fields['artist'].widget = TextInput(attrs={'class': 'create-field piece-artist'})
        form.fields['album'].widget = TextInput(attrs={'class': 'create-field piece-album'})
        form.fields['notes'].widget = Textarea(attrs={'class': 'create-field piece-notes'})
        return form


class PieceDelete(LoginRequiredMixin, DeleteView):
    model = Piece
    context_object_name = 'piece'
    success_url = reverse_lazy('piece list')
    login_url = reverse_lazy('info')







