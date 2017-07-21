from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Event, Category

# Create your views here.

class HomeView(TemplateView):
	template_name = 'pages/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['events'] = Event.objects.all().order_by('-created')[:6] # for 6 last created
		context['categories'] = Category.objects.all() 
		return context