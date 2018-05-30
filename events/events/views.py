from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Category
from events.users.models import User
from .forms import EventForm


# Create your views here.

class HomeView(TemplateView):
	template_name = 'pages/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['events'] = Event.objects.all().order_by('-created')[:6] # for 6 last created
		context['categories'] = Category.objects.all() 
		return context

class CreateEvent(LoginRequiredMixin, CreateView):
	form_class = EventForm
	model = Event
	template_name = 'events/create_event.html'

	def get_success_url(self):
		return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(CreateEvent, self).form_valid(form)


class DetailEvent(DetailView):
	model = Event
	template_name = 'events/detail_event.html'
	context_object_name = 'event'