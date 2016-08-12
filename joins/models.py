from __future__ import unicode_literals

from django.db import models

# Create your models here.
# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)
    
class Join(models.Model):
	bedrooms = models.CharField(max_length=6, null=True)
	bathrooms = models.CharField(max_length=4, null=True)
	ft2 = models.IntegerField(null = True)
	neighborhood = models.CharField(max_length=100, null=True, default='nyc')
	price = models.IntegerField(null = True)
	email = models.EmailField(blank = True, null = True)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)
	title = models.CharField(max_length=120, null = True, blank = True)
	hashid = models.BigIntegerField(primary_key = True)
	name = models.CharField(max_length = 30, null = True, blank = True)
	parent_neighborhood = models.CharField(max_length=200, null=True)
	full_address = models.CharField(max_length=100, null = True)
	listing_type_text = models.CharField(max_length=19, default='Apartment')
	# created_at = models.BigIntegerField(blank = True, null = True)
	created_at = models.CharField(max_length=40, null=True)
	url = models.CharField(max_length=250, null = True)
	image_url = models.CharField(max_length = 250, null = True)
	# duplicate_similarity= models.FloatField(null = True)
	# duplicate_id = models.BigIntegerField(null = True)
	source = models.CharField(max_length=20, default = "joinery")# {0: 'Joinery', 1: 'craigslist', 2: 'streeteasy', 3: 'nybits', 4: 'nakedapartments'}
	section = models.CharField(max_length=40, null=True)
	excerpt = models.CharField(max_length=500, null=True)
	isbroker = models.BooleanField(default=False)
	isscam = models.BooleanField(default=False)
	isemailsent = models.BooleanField(default=False)
	hide = models.BooleanField(default=False)
	emailtext=models.CharField(max_length=1000, null = True)
	duplicategroupid= models.IntegerField(null = True,  default=0)
	score = models.FloatField(null = True, default = 0)
	views = models.IntegerField(null = True)
	messages = models.IntegerField(null = True)
	images = models.IntegerField(null = True)
	slug = models.CharField(max_length = 100, null = True)
	available_date = models.CharField(max_length = 20, null = True)
	latitude = models.FloatField(null = True)
	longitude = models.FloatField(null = True)
	# sendemail = models.DateTimeField(null = True, blank = True)
	# BED_CHOICES = (('S', 'Studio'),('1', '1 bedroom'), ('2', '2 bedrooms'), ('3', '3 bedrooms'), ('4', '4 bedrooms or more'), ('L', 'Loft'),)
	# bedroom = models.CharField(max_length = 1, choices = BED_CHOICES, blank = True)
	# BATH_CHOICES = (('S', 'Shared bathroom'),('1', '1 bathroom'), ('2', '2 bathroom'), ('3', '3 bathrooms or more'),)
	# bathroom = models.CharField(choices = BATH_CHOICES, max_length = 1, blank = True)
	# TYPE_CHOICES = (('A', 'Apartment'),('R', 'Room'),)
	# listing_type_text = models.CharField(choices = TYPE_CHOICES, max_length = 1, default = 'A')
	# # updated_at = models.DecimalField()
	# available_date = models.BigIntegerField(null = True)
	# image = 
	# friend = models.ForeignKey("self", related_name='referral',\
	# 									null=True, blank=True)3
	# ref_id = models.CharField(max_length=120, default='ABC', unique=True)
	# ip_address = models.CharField(max_length=120, default='ABC')

	def __unicode__(self):
		# return "%s %s %s %s %s %d"%(self.email, self.bedroom, self.bathroom, self.title. self.neighborhood, self.price)
		return "%s %s %d"%(self.created_at, self.title, self.price)

	# class Meta:
	# 	unique_together = ("email", "ref_id",)

class Neighborhood(models.Model): 
	#source : streeteasy = 2, nybits = 3, nakedapartments =4 , craigslist = 1
	hashid = models.IntegerField(null= True, default = 0)
	shid = models.IntegerField(null = True)
	source = models.CharField(max_length=20, default = "joinery")
	area = models.CharField(max_length=50)
	nid = models.CharField(max_length=20)
	parentarea = models.CharField(max_length=50)
	latitude = models.FloatField(null = True, default=0.)
	longitude = models.FloatField(null = True, default=0.)
	updated = models.NullBooleanField(default = False)



class Userhist(models.Model):
	userid = models.BigIntegerField(null = True) 
	seenhist = models.CharField(max_length=1000, null = True)
	alerthist =  models.CharField(max_length=1000, null = True)
	searchhist = models.CharField(max_length=1000, null = True)
	savehist = models.CharField(max_length = 1000, null = True)







