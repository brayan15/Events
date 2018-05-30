from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from events.users.models import User

# Create your models here.

class TimeStart(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		#this is when I run migrate this class not will be create,
		#and only will be inherit on other models


class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(editable=False)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name
	#for python 3
	#def __str__(self):
	#	return self.name


class Event(TimeStart):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50, unique=True,blank=False)
	slug = models.SlugField(editable=False)
	description = models.TextField(max_length=300)
	content = models.TextField()
	category = models.ForeignKey(Category)
	city = models.CharField(max_length=20, blank=False)
	place = models.CharField(max_length=50,blank=False)
	date = models.DateField(blank=False)
	start = models.TimeField(blank=True)
	end = models.TimeField(blank=True)
	image = models.ImageField(blank=True)
	free = models.BooleanField(default=True)
	price = models.DecimalField(max_digits=5,decimal_places=2, default=0.00)
	view = models.PositiveIntegerField(default=0)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Event, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name


class Assistant(TimeStart):
	assistant = models.ForeignKey(User)
	event = models.ManyToManyField(Event)
	attended = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)

	""" def __unicode__(self):
		return '%s %s' % (self.assistant, self.event.name) """


class Comment(TimeStart):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	content = models.TextField(max_length=200)

	def __unicode__(self):
		return '%s %s' % (self.user.username, self.event.name)
		


