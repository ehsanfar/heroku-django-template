from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
# from .scr2db
from .models import Join, Neighborhood
from .forms import JoinForm, AptForm, SearchForm
import codes

# Create your views here.
def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip


#str(user_id)[:11].replace('-', '').lower()
import uuid

def get_ref_id():
	ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
	#ref_id = '9f16a22615'
	try:
		id_exists = Join.objects.get(ref_id=ref_id)
		get_ref_id()
	except:
		return ref_id



def share(request, ref_id):
	#print ref_id
	try:
		join_obj = Join.objects.get(ref_id=ref_id)
		friends_referred = Join.objects.filter(friend=join_obj)
		count = join_obj.referral.all().count()
		ref_url = settings.SHARE_URL + str(join_obj.ref_id)

		context = {"ref_id": join_obj.ref_id, "count": count, "ref_url": ref_url}
		template = "share.html"
		return render(request, template, context)
	except:
		raise Http404

def renderdb(request, message=''): 
	apt_list = Join.objects.all()
	apt_list = apt_list.order_by('-created_at')
	paginator = Paginator(apt_list, 50)

	page = request.GET.get('page')
	try:
	    apts = paginator.page(page)
	except PageNotAnInteger:
	    apts = paginator.page(1)
	except EmptyPage:
	    apts = paginator.page(paginator.num_pages)
	# context = {"form":form}
	context  = {'apts' : apts, 'message': message}
	template = "list.html"
	return render(request, template, context)

def updatedb(request):
  	print "The function is called"
  	# status, difftime = codes.cl2db()
  	codes.url2db()
	if status==1:
		message = "Database is updated after %d minuts from previous update."%difftime
	else:
		message = "Database was recently updated: %d minutes, try again later!"%difftime
	return redirect('/')

def updatedup(request):
  	codes.updateduplicates(0.7)
	return redirect('/')

def setscam(request, page_id):
  	codes.setscam(page_id)
	return redirect('/%s/'%page_id)

def setbroker(request,  page_id):
	codes.setbroker(page_id)
	return redirect('/%s/'%page_id)

def setemailsent(request,  page_id):
	codes.setemailsent(page_id)
	return redirect('/%s/'%page_id)


def setscam2(request, page_id):
  	codes.setscam(page_id)
	return redirect('/')

def setbroker2(request,  page_id):
	codes.setbroker(page_id)
	return redirect('/')

def setemailsent2(request,  page_id):
	codes.setemailsent(page_id)
	return redirect('/')

# def deleteapt(request, page_id):


def apt(request, page_id):
	question = get_object_or_404(Join, hashid=page_id)
	template = 'apt.html'
	pagedata=Join.objects.get(hashid=page_id)
	dgid = pagedata.duplicategroupid
	if dgid==0:
		context = {'apt': pagedata}
	else:
		alldups = Join.objects.filter(duplicategroupid = dgid).exclude(hashid = page_id)
		BASEURL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		context = {'apt': pagedata, 'duplicates': alldups, 'baseurl':BASEURL}
	# print pagedata.hashid, pagedata.duplicate_similarity, pagedata.duplicate_id
	return render(request, template, context)



def list(request):
 #    try:
 #    	join_id = request.session['join_id_ref']
 #    	obj = Join.objects.get(id=join_id)
 #    except:
 #    	obj = None
	
	# form = JoinForm(request.POST or None)
	# if form.is_valid():
	# 	new_join = form.save(commit=False)
	# 	email = form.cleaned_data['email']
	# 	print email 
	# 	if email:
	# 		new_join_old, created = Join.objects.get_or_create(email=email)
	# 		if created:
	# 			new_join_old.ref_id = get_ref_id()
	# 			# add our friend who referred us to our join model or a related
	# 			if not obj == None:
	# 				new_join_old.friend = obj
	# 			new_join_old.ip_address = get_ip(request)
	# 			new_join_old.save()
	form = JoinForm(request.POST or None)
	# print form , type(form)
	if form.is_valid():
		new_join = form.save(commit=False)
		print new_join
		new_join.save()
		
		#print all "friends" that joined as a result of main sharer email
		#print Join.objects.filter(friend=obj).count()
		#print obj.referral.all().count()

		#redirect here
		# return HttpResponseRedirect("/%s" %(new_join_old.ref_id))
	return renderdb(request) 


def editinfo(request, page_id):
	form = AptForm(request.POST or None)
	aptinfo = Join.objects.get(hashid = page_id)
	# if request.method == 'POST':
	if form.is_valid():
		data = form.cleaned_data#. to_dict(flat=True)
		print data
		# image_url = upload_image_file(request.files.get('image'))
		# if image_url:
		#     data['imageUrl'] = image_url
		codes.updatelisting(data, page_id)
		return redirect('/%s/'%page_id)

	return render(request, "form.html", {'apt': aptinfo})

def search(request):
	form = SearchForm(request.POST or None)
	aptinfo = Join.objects.first()
	# if request.method == 'POST':
	if form.is_valid():
		data = form.cleaned_data#. to_dict(flat=True)
		if not data["neighborhood"]:
			data["neighborhood"]='nyc'
		if not data["minprice"]: 
			data["minprice"] = 0
		if not data["maxprice"]:
			data["maxprice"]= 20000
		if not data["bedroom"]:
			data["bedroom"]=1
		if not data["bathroom"]:
			data["bathroom"]=1

		print data

		urls = codes.create_url(data["neighborhood"], data["minprice"], data["maxprice"], data["bedroom"], data["bathroom"])
		render(request, "search.html", {'apt':data, 'urls': urls})

	return render(request, "search.html")

def updateneighbors(request):
	codes.updateneighbors()
	return redirect('/')


def sendrequesttoanni(request):
  	codes.sendrequesttoanni()
	return redirect('/')

# def editinfo(request, page_id): 
# 	form = JoinForm(request.POST or None)
# 	print form 
# 	a = Join.objects.get(hashid = page_id)
# 	if form.is_valid():	
# 		form_clean = form.cleaned_data
# 		name = form_clean[ 'name']
# 		email = form_clean['email']
# 		neighborhood = form_clean['neighborhood']
# 		bedroom = form_clean ['bedroom']
# 		neighborhood = form_clean['neighborhood']
# 		bathroom = form_clean ['bathroom']

# 		if len(name)>0:
# 			a.name = name
# 		if len(email)>0: 
# 			a.email = email 
# 		if len(neighborhood) >0:
# 			a.neighborhood = neighborhood
# 		if len(bedroom) >0:
# 			a.bedroom = bedroom
# 		if len(bathroom) >0:
# 			a.bathroom = bathroom

# 		a.save()

# 	return redirect('/%s/'%page_id)




	# if form.is_valid():
	# 	a = Join.objects.get(hashid = page_id)
		 