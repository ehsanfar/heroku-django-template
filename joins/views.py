from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
# from .scr2db
from django.http import JsonResponse, HttpResponse #Sends back JSON response, might be useful
from django.views.decorators.csrf import csrf_exempt #Stops the Refferrer error for https, another work around would be to go to the config files and manually entering it there
import json #For JSON

from .models import Join, Neighborhood, Userhist
from .forms import JoinForm, AptForm, SearchForm
import codes
import scodes

#temporary for debugging
from inspect import currentframe, getframeinfo

from rq import Queue
from worker import conn
from worker import checkRedis


q = Queue(connection=conn)


SORTATT = '-created_at'

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

def renderdb(request, apt_list = None, template = 'list.html'): 
	global SORTATT
	if not apt_list:
		apt_list = Join.objects.all()

	order_by = request.GET.get('order_by',SORTATT)
	SORTATT = order_by
	apt_list = apt_list.order_by(order_by)
	paginator = Paginator(apt_list, 100)

	page = request.GET.get('page')
	try:
	    apts = paginator.page(page)
	except PageNotAnInteger:
	    apts = paginator.page(1)
	except EmptyPage:
	    apts = paginator.page(paginator.num_pages)
	# context = {"form":form}
	context  = {'apts' : apts}
	template = template 
	return render(request, template, context)

def renderresults(request, hashlist = [], message='No message yet!'): 
	apt_list = []
	# objs = Join.objects.all()
	hashlist = hashlist if hashlist else []
	for h in hashlist: 
		print "Hashcode:", h
		a = Join.objects.get(hashid = h)
		apt_list.append(a)

	# context = {"form":form}
	print "The listing is: ", apt_list
	# context  = {'apts' : apt_list, 'message': message}
	context  = {'apts' : apt_list, 'message': message}
	template = 'results.html' 
	print 'The template is:', template
	return render(request, template, context)
	# return redirect('/')



def updatedb(request):
  	# print "The function is called"
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
		# print new_join
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
		# print data
		# image_url = upload_image_file(request.files.get('image'))
		# if image_url:
		#     data['imageUrl'] = image_url
		codes.updatelisting(data, page_id)
		return redirect('/%s/'%page_id)

	return render(request, "form.html", {'apt': aptinfo})

@csrf_exempt #For the https:// problem, this is mainly for receiving JSON from Node.js or an outside server
def search(request):
	requestObj = ''
	print "Search Received"
	try:
		requestObj = request.body.decode('utf-8')
		data = json.loads(requestObj) #Prints the data received
		print "The data is: ", data
		#print "JSON received"
		print "Json Received and the tag is:", data["tag"]

		if "tag" not in data: 
			# data["tag"] = "search" 
			print 'No TAG'
			redirect('/')

		elif  data["tag"]!='find' and (("userid" in data) or (data['tag'] == 'listing')): 
			print "This is for none search: ", data, getframeinfo(currentframe()).lineno
			codes.saveuserdata(data)

		elif data["tag"] == 'match_address': 
			codes.saveuserdata(data)
			return redirect('/')

		elif data["tag"] =='response':
			return redirect('/')

		if data["tag"] not in ['search', 'find']:
			# print "line:", getframeinfo(currentframe()).lineno
			JsonResponse({'message':"The database is updated"})
			return redirect('/')

		elif data["tag"]=='find': 
			print "Doesn't belong here"
			return redirect('/find/')

			# return redirect('/fresults/')



		else: 
			if "neighborhood" not in data:
				data["neighborhood"]='nyc'
			if "minprice" not in data: 
				data["minprice"] = 0
			if "maxprice" not in data:
				data["maxprice"]= 20000     
			if "bedrooms" not in data:
				data["bedrooms"]='1'
			if "bathrooms" not in data:
				data["bathrooms"]=None

                        strsearchhashid = str(codes.calsearchhashid(data))
                        #addedhashlist = []
                        #print strsearchhashid
            
                        if not checkRedis(strsearchhashid):
                                addedhashlist, N = q.enqueue(codes.create_url, data["neighborhood"], data["minprice"], data["maxprice"], data["bedrooms"], data["bathrooms"]) 
                        else: print '%s is already searched before' % strsearchhashid
                        #addedhashlist, N=codes.create_url(data["neighborhood"], data["minprice"], data["maxprice"], data["bedrooms"], data["bathrooms"])
			
			# print "The new hashid lists and the total number of results are: ", getframeinfo(currentframe()).lineno, addedhashlist, N
                        returnhashlist = codes.findlisting(data)
                        resdict = {}
                        for i in range(len(returnhashlist)):
                                resdict[i] = returnhashlist[i]

                        print resdict
                        return JsonResponse(resdict) #Debug, something else can be sent as JSON
                        return redirect('/')

	except ValueError:
		# print(reqest.body, request.GET, request.POST)
		print requestObj
		print 'no JSON' #No JSON received
		return redirect('/')

	# form = SearchForm(request.POST or None)
	# aptinfo = Join.objects.first()
	# # if request.method == 'POST':
	# if form.is_valid():
	# 	data = form.cleaned_data#. to_dict(flat=True)
	# 	if "neighborhood" not in data:
	# 		data["neighborhood"]='nyc'
	# 	if "minprice" not in data: 
	# 		data["minprice"] = 0
	# 	if "maxprice" not in data:
	# 		data["maxprice"]= 20000
	# 	if "bedroom" not in data:
	# 		data["bedroom"]='1'
	# 	if "bathroom" not in data:
	# 		data["bathroom"]=1

	# 	print "This is the form data after edit: ", getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno, data
	# 	items = codes.create_url(data["neighborhood"], data["minprice"], data["maxprice"], data["bedroom"], data["bathroom"])
	# 	# hashidlist, N = codes.create_url(data["neighborhood"], data["minprice"], data["maxprice"], data["bedroom"], data["bathroom"])
	# 	return render(request, "search.html")

	return render(request, "search.html")

def updateneighbors(request):
	# codes.updateneighbors(
	# codes.updateneighbcoordinates()
	# codes.makeListofSamePArea()
	# codes.updatejoinery()
	scodes.updateaddresscoordinates()
	return redirect('/')

def updatehashids(request):
	codes.updatehashids()
	return redirect('/')

def sendrequesttoanni(request):
	tag = request.GET.get('tag', 'search')
	if tag == 'listing': 
		codes.updatejoinery()
	elif tag == 'find': 
		data = codes.sendrequesttoanni(tag)
		hashlist = codes.findranklisting(data)
		# hashlist = [200000131]
		print "The found listings: ", hashlist
		message = json.dumps(data)

		print "The message:", message
		return renderresults(request, hashlist = hashlist, message = message)

	else:
	  	codes.sendrequesttoanni(tag)
	return redirect('/')


def sort_view(request):
    form = SortForm()
    return render_response(request, 'list.html',{'form': form})


def updateshortneighborhoodid(request):
	codes.updateShortNHash()
	return redirect('/')

def updateparentneighborhood(request):
	codes.updateparentneighborhood()
	return redirect('/')

@csrf_exempt #For the https:// problem, this is mainly for receiving JSON from Node.js or an outside server
def find(request):
	requestObj = ''
	print "Find REceived"
	try:
		requestObj = request.body.decode('utf-8')
		data = json.loads(requestObj) #Prints the data received
		print "The data is: ", data
		hashlist = codes.findranklisting(data)
		# hashlist = [200000131]
		print "The found listings: ", hashlist
		message = json.dumps(data)

		print "The message:", message
		return renderresults(request, hashlist = hashlist, message = message)

	except ValueError:
		# print(reqest.body, request.GET, request.POST)
		print "The request object is:", requestObj
		print 'no JSON' #No JSON received
		hashlist = []
		message = 'No message!'
		return renderresults(request, hashlist, '')

	# return renderresults(request, hashlist = hashlist, message = message)

	

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
		 
