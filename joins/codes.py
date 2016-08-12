from .models import Join, Neighborhood, Userhist

import sys, json, base64, os, urllib2
# from ipywidgets import widgets
from bs4 import BeautifulSoup
# import codecs
import urllib
import scodes
import datetime 
import time 
import random 
import re
# import pandas as pd
# from nltk import word_tokenize
# from scipy import stats
# import nltk
# import collections 
from math import isnan 
from django.db.models import Q
# nltk.data.path.append('./nltk_data/')
# this part is for debuggin should be removed afterwards 
from inspect import currentframe, getframeinfo


# end of debugging part 


reload(sys)  
sys.setdefaultencoding('utf8')

global DIV
DIV = 1000000
SORTATT = 'created_at'


def call_agent(url, data=None, wait='feedItem-details'):
    if 'zumper' in url:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        #print 'zumper'
        driver = webdriver.PhantomJS()
        driver.get(url)
        try:
            print 'waiting for feedItem'
            element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, wait))
            )
        finally:
             html = driver.page_source
             soup = BeautifulSoup(html, "html.parser")
             soup = soup.find('div', {'class' : 'content-wrap'})
             driver.quit()

    else:
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request(url, data, headers)
        html = urllib2.urlopen(req).read()  
        soup = BeautifulSoup(html, "html.parser")

    return soup


def name_similarity(rname, neighborhood): # real name vs similar name 
    rname = rname.lower()
    neighborhood = neighborhood.lower()
    N=max(len(rname),len(neighborhood))
    Ns=[]
    # n = 10
    shift = range(-5, 6)
    # shift=[-1,0,1]
    accuracy=[]
#     print rname, sname 
    w1 = rname
    w2 = neighborhood
    for j in range(2):
        temp = w1
        w1 = w2
        w2 = temp 

        for i in range(len(shift)):
            sh=shift[i]
            sn = ''
            if sh<0:
                l=len(w2)
                for i in range(len(w1)):
                    if i>=l:
                        break
                    if w1[i]!=w2[i]:
                        sn = w1[:i]+w1[i+sh:]
                        break

            elif sh>0:
                l=len(w2)
                for i in range(len(w1)):
                    if i>=l:
                        break
                    if w1[i]!=w2[i]:
                        sn = w1[:i]+abs(sh)*' '+w1[i:]
                        break

            else:
                sn=w1

            Ns.append(0.)
            for i in range(min(len(w2), len(sn))): 
                if sn[i] == w2[i]: 
                    Ns[-1]+=1

            # print sh
            # print sn
            # print neighborhood

            accuracy.append(Ns[-1]/N)

            # print accuracy[-1]
    
    return max(accuracy)
            
    
# def match_address(w, adrs): 
#     adrs=adrs.lower()
#     p=0.8
#     if w==0:
#         adrsNames=pd.read_csv("Files/streeteasy_neighborhood.csv", index_col=0)
#         neighbNames=list(adrsNames["neighborhood"])

#         newNeighbs=[x for x in neighbNames]
#         nameDict={}
#         for n in newNeighbs:
#             nameDict[n]=name_similarity(adrs, n)        

#         sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
#         if sortedNeighbs: 
# #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
#             if nameDict[sortedNeighbs[0]]>p:
#                 level=list(adrsNames[adrsNames['neighborhood']==sortedNeighbs[0]]["level"])[0]
#                 return (level, sortedNeighbs[0],-1)
#             else: 
#                 return (-1,-1,-1)
#         else: 
#             return -1
#     elif w==1:
#         adrs=adrs.lower()
#         adrsNames=pd.read_csv("Files/neighborhood_nybits.csv", index_col=0)
#         neighbNames=[s.replace('_', ' ') for s in list(adrsNames["Neighbor_codes"])]
#         newNeighbs=neighbNames[::]
#         nameDict={}
#         for n in newNeighbs:
#             nameDict[n]=name_similarity(adrs, n)        

#         sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
#         if sortedNeighbs: 
# #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
#             if nameDict[sortedNeighbs[0]]>p: 
#                 row=adrsNames[adrsNames['Neighbor_codes']==sortedNeighbs[0].replace(' ', '_')]
#                 code=list(row["Neighbor_codes"])[0]
#                 level=list(row["level"])[0]
#                 return (level, sortedNeighbs[0], code)
#             else:
#                 return (-1,-1,-1)
#         else: 
# #             print "we didn't find any matching name, try again please"
#             return -1

#     elif w == 'streeteasy':
#         adrs=adrs.lower()
#         adrsNames=pd.read_csv("Files/neighborhood_nakedapartments.csv", index_col=0)
#         neighbNames=list(adrsNames["Neighbor_names"])
#         newNeighbs=neighbNames[::]
#         nameDict={}
#         for n in newNeighbs:
#             nameDict[n]=name_similarity(adrs, n)        

#         sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
#         if sortedNeighbs: 
# #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
#             if nameDict[sortedNeighbs[0]]>p: 
#                 row=adrsNames[adrsNames['Neighbor_names']==sortedNeighbs[0]]
#                 code=list(row["Neighbor_codes"])[0]
#                 level=list(row["level"])[0]
#                 return (level, sortedNeighbs[0], code)
#             else: 
#                 return(-1,-1,-1)
        

#         else: 
# #             print "we didn't find any matching name, try again please"
#             return -1
#     elif w == 'nybits': 
#         ny_neighborhood_names = open("Files/ny_neighborhood_names.txt", "r")
#         newNeighbs=ny_neighborhood_names.read().split('\n')

#         querywords=word_tokenize(adrs)
#         revisedwords=[]
#         for w in querywords:
#             nameDict={}
#             for n in newNeighbs:
#                 nameDict[n]=name_similarity(w, n) 
#             sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
#             revisedwords.append(sortedNeighbs[0])
        
#         return (0, '', ' '.join(revisedwords)) 

                
#     else: 
#         return -1
        

def find_bedrooms_from_title(title):
    roomterms=["br", "rooms", "bedrooms", "bdrm"]
    title=title.lower()
    if "studio" in title: 
        output="studio"
        return output
    
    temp=re.search('\d+\s?br', title)
    if temp: 
        output=temp.group(0).replace(' ', '')
        return output
    else: 
        temp=re.search('\d+\s?bdrm', title)
        if temp: 
            output=temp.group(0)
        else: 
            title=title.lower()
            temp=re.search('\d+\s?bedroom', title)
            if temp: 
                output= temp.group(0)
            else:
                #print "There is no bedroom in: ", title
                output=None
    
    if "loft" in title: 
        if output:
            nbeds=re.search('\d+', output).group(0) 
            return nbeds+"br loft"
        else: 
            return "loft"
    else: 
        if output: 
            nbeds=re.search('\d+', output).group(0) 
            return nbeds+"br"
        else: 
            return None



def find_apt_or_room(title):
    title=title.lower()
    terms=[" room ", " bedroom ", "roommate" ]
    roomcount = title.count("room")
    brcount = title.count("br") 
    for t in terms: 
        if (t in title) or (roomcount>1) or (brcount>1): 
            return "Room"
        else: 
            return "Apartment"
    
def findlasttime(currenttime, ndays):
    year=currenttime.year
    month=currenttime.month
    day=currenttime.day
    
    ndays=min(ndays,7)
    if day>ndays:
        return "%s-%s-%s"%(year, str(month).zfill(2), str(day-ndays).zfill(2))
    else:
        return "%s-%s-%s"%(year, str(month-1).zfill(2), str(day-ndays+30).zfill(2))

def cal_simil(item1, item2):
    nit1=len(item1)
    minlength=min(len(item1), len(item2))
    if minlength==0: 
        return 0

    elif minlength==nit1: 
        shorter=item1
        longer=item2
    else: 
        shorter=item2
        longer=item1

    nwords=0
    for word in shorter: 
        if word in longer: 
            nwords+=1
    return float(nwords)/len(longer)


def brokertobool(broker_prob):
	if broker_prob>50: 
		return True
	else: 
		return False

def convertbeds(beds):
    if beds is None:
        return 'N'
    else:
        if beds[0].isdigit():
            return beds[0]
        else: 
            return beds[0].upper()
            

def add_broker(df):
    duplicate=[]
    duplicatetime=[]
    titlelist=list(df['title'])
    nonasciititles=[re.sub(r'[^\x00-\x7F]+',' ', text) for text in titlelist]
    
    # alltitles=word_tokenize(' '.join(nonasciititles).lower())
    alltitles=' '.join(nonasciititles).lower().split()
    brokerfactor=[]
    titlerepetitionfactor=[]
    titlekeywordfactor=[]
    titlecapitalized=[]
    allwords=[]
    
    # allwords=word_tokenize(' '.join(nonasciititles))
    allwords=' '.join(nonasciititles).split()
    wordcount = {}
    for w in allwords:
        if word not in wordcount:
            wordcount[w] = 1
        else:
            wordcount[w] += 1

    
    for s in nonasciititles: 
        cl=sum([1 for c in s if c.isupper()])
        sl=len(s)
        titlecapitalized.append(float(cl)/sl)
        # words=word_tokenize(str(s))
        words = str(s).split()
        titlerepetitionfactor.append(sum([wordcount[w] for w in words]))

    maxcount=float(max(titlerepetitionfactor))
    sortedlist = sorted(titlerepetitionfactor)
    repetitionpercentile = []
    for t in titlerepetitionfactor: 
        repetitionpercentile.append(sortedlist.index(t)/float(len(titlerepetitionfactor)))

    # repetitionpercentile=[stats.percentileofscore(titlerepetitionfactor, a, 'strict') for a in titlerepetitionfactor]

    brokerscore=[int((repetitionpercentile[i]+100*titlecapitalized[i])/2) for i in range(len(repetitionpercentile))]
    filteredbrokerscore=[]
    for x in brokerscore: 
        if x>=40:
            filteredbrokerscore.append(x)
        else: 
            filteredbrokerscore.append(0)
            
    df=df.copy()
    isbroker=[brokertobool(b) for b in filteredbrokerscore]
    df['isbroker']=isbroker
#     figure()
#     hist(filteredbrokerscore)
#     show()
    return df

def convertrowstodf(rows, section, sectionlastdate):
    import pandas as pd
    ID=[]
    hreflinks=[]
    titles=[]
    prices=[]
    datetimes=[]
    neighborhoods=[]
    beds=[]
    aptorroom=[]
    dublicate=[]
    owner=[]
    duplicate=[]
    duplicatetime=[]
    broker=[]
    # section=[]

    for r in rows:
        title=r.find("span", {"id":"titletextonly"}).text
        titles.append(title)
        beds.append(find_bedrooms_from_title(title))
        aptorroom.append(find_apt_or_room(title))
        hreflinks.append("http://newyork.craigslist.org"+r.a["href"])
        datetimes.append(r.time["datetime"]) 
        reneighb = re.search(r"\(.*\)", r.find("span", {"class":"pnr"}).text)
        reprice=r.find("span", {"class":"price"})
        if reprice:
            prices.append(int(reprice.text[1:]))
        else: 
            prices.append(None)

        if reneighb:
            neighborhoods.append(reneighb.group(0)[1:-1])
        else:
            neighborhoods.append(None)
        duplicate.append(0)
        duplicatetime.append(0)
        broker.append(0)
        # section.append(sections[i])
        ID.append(calhashid(beds[-1], neighborhoods[-1], None, prices[-1], source))

    # isbroker=[brokertobool(b) for b in broker]
    beds = [convertbeds(b) for b in beds]
    ID=[int(i) for i in ID]
    # print ID
    pagedict={"hashid": ID, "title":titles, "created_at": datetimes, "listing_type_text": aptorroom, "bedroom": beds, "price":prices, "neighborhood": neighborhoods, "linkurl": hreflinks}
    index = [ind for ind, d in enumerate(pagedict['hashid']) if d >= sectionlastdate*DIV ]
       #df['section'] = section
       #df = df[df['hashid'] >= sectionlastdate*DIV]
    if len(index)==0:
        return pagedict

    dfdict = []
    for i in index:
        dfdict.append({'hashid':pagedict['hashid'][i], 'title':pagedict['title'][i],'created_at':pagedict['created_at'][i],'listing_type_text':pagedict['listing_type_text'][i], 'bedroom': pagedict['bedroom'][i], 'price':pagedict['prices'][i], 'neighborhood': pagedict['neighborhoods'][i], 'linkurl': pagedict['linkurl'][i], 'section': section})
    # dfdict = [d for d in dfdict if d
    for dic in dfdict: 
        if len(Join.objects.filter(hashid = dic['hashid']))>0:
            continue

        clean_dict = {k: dic[k] for k in dic if isinstance(dic[k], basestring) or str(dic[k]).isdigit()}
        clean_dict.update({k: dic[k] for k in dic if isinstance(dic[k], float) and not isnan(dic[k])})
        if 'hashid' in clean_dict:
        # print dic
            a=Join(**clean_dict)
            try:
                a.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
        else: 
            print "No hashid: ", clean_dict

    return dfdict

def findtimediffinminutes(ct, lt):
    mindif = ct%100 - lt%100 
    ct = ct / 100 
    lt = lt / 100
    hourdif = ct%100 - lt%100 
    ct = ct / 100 
    lt = lt / 100
    daydif = ct%100 - lt%100 
    ct = ct / 100 
    lt = lt / 100
    monthdif = ct%100 - lt%100 
    ct = ct / 100 
    lt = lt / 100
    yeardiff = ct - lt

    return mindif + 60*(hourdif + 24*(daydif + 30* (monthdif+ 12*yeardiff)))
    
def updateduplicates(threshold):
    allobjects = Join.objects.all().order_by('-hashid')
    if len(allobjects)<=1: 
        return 

    maxduplicategroupid = Join.objects.all().order_by('-duplicategroupid')[0].duplicategroupid
    pricelist = [o.price for o in allobjects]
    titlelist = [o.title for o in allobjects]
    neighborlist = [o.neighborhood for o in allobjects]
    hashlist = [o.hashid for o in allobjects]
    duplicatelist=[o.duplicategroupid for o in allobjects]
    # pricelist=list(df['price'])
    # titlelist=list(df['title'])
    nonasciititles=[re.sub(r'[^\x00-\x7F]+',' ', text) for text in titlelist]
    titlelist_token=[t.split() for t in nonasciititles if len(t)>0]
    # neighborlist=list(df['neighborhood'])
    # neighborlist_token=[word_tokenize(str(n)) for n in neighborlist if len(str(n))>0]
    neighborlist_token=[str(n).split() for n in neighborlist if len(str(n))>0]
    # datelist=list(df['hashid'])
    N=len(pricelist)
    for i in range(N): 
        if duplicatelist[i]>0:
            continue

        neighb=neighborlist_token[i]
        price=pricelist[i]
        title=titlelist_token[i]
        for j in range(N): 
            if (duplicatelist[i]>0 and duplicatelist[j]>0) or j==i:
                continue
            newprice=pricelist[j]
            newtitle=titlelist_token[j]
            newneighb=neighborlist_token[j]
            d2=cal_simil(neighb, newneighb)
            if d2>threshold:
                d1=cal_simil(title, newtitle)
                if newprice==price:
                    d3=1
                    similarity=sum([d1, d2, d3])/3.
                else: 
                    similarity=sum([d1, d2])/2.
                    
                if similarity>threshold: 
                    if duplicatelist[j]>0 and duplicatelist[i]==0:
                        duplicatelist[i] = duplicatelist[j]
                        break

                    if duplicatelist[i]>0 and duplicatelist[j]==0:
                        duplicatelist[j] = duplicatelist[i]
                    else: 
                        maxduplicategroupid +=1
                        duplicatelist[i] = maxduplicategroupid
                        duplicatelist[j] = maxduplicategroupid

    for i in range(N):
        # allobjects[i].duplicategroupid = duplicategroupid[i]
        # print hashlist[i] 
        b = Join.objects.get(hashid = hashlist[i])
        b.duplicategroupid =  duplicatelist[i]
        b.save()

def cl2db(): 
    urls=[]
    urls.append("http://newyork.craigslist.org/search/abo?sort=date&query=apartment")
    urls.append("http://newyork.craigslist.org/search/roo?sort=date&query=apartment")
    tagnames=["abo","roo"]
    sections=["apt by owner", "rooms & shares"]
    sectiondict={"abo": "apt by owner", "roo": "rooms & shares"}
    # finalhtmls={}
    dataframes=[]
    n=len(urls)
    cdt = datetime.datetime.now()
    currenttime = int(str(cdt.year) + str(cdt.month).zfill(2) + str(cdt.day).zfill(2) + str(cdt.hour).zfill(2) + str(cdt.minute).zfill(2))
    dbhist=Join.objects.all()
    # DIV = 1000000
    if len(dbhist)>0:
        dt = dbhist.order_by('-timestamp')[0].timestamp
        lasttime = int(str(dt.year) + str(dt.month).zfill(2) + str(dt.day).zfill(2) + str(dt.hour).zfill(2) + str(dt.minute).zfill(2))
        # print currenttime, lasttime, cdt, dt
        difftime = findtimediffinminutes(currenttime, lasttime)
        if difftime<120: 
            return (2, difftime) #2 means that the db is recentely 
    else: 
        difftime = -1

    for i in range(n):
        j=0
        listhist=Join.objects.filter(section=sections[i]) 
        if len(listhist)>0:
            sectionmaxhashid = listhist.order_by('-hashid')[0].hashid
            sectionlastdate = sectionmaxhashid/DIV
        else: 
            sectionmaxhashid = 201601010000*DIV
            sectionlastdate = 201601010000

        url=urls[i]
        masterdict = []
        while j<300:
            sleeptime=10+10*random.random()
            # print "I am sleeping for %f seconds"%sleeptime
            time.sleep(sleeptime)
            url2=url+"&s="+str(j)
            print url2
            # filename=filenames[i]
            # finalhtmls.append(call_agent(url))
            soup = call_agent(url)
            rows = soup.findAll("p", {"class":"row"})
            if len(rows)>0:
                lastrowdate = rows[-1].time["datetime"]
            else: 
                print "No row in the html page"
                break

            dic = convertrowstodf(rows, sections[i], sectionlastdate) # return list of dictionaries each dictionary one row of listing more recent than the last listing in db 

            if len(dic)>0:
                masterdict += dic 
            else: 
                print "No row was newer thatn the last section row in database : ", df['hashid'], sectionlastdate*DIV
                break 

            if int(sid)<=sectionlastdate:
                print "The last row is older than the section last update in database : %d > %d"%(int(sid), sectionlastdate) 
                break
             # if not didit:
            #     break
            j+=100


    for dic in masterdic: 
        if len(Join.objects.filter(hashid = dic['hashid']))>0:
            continue

        clean_dict = {k: dic[k] for k in dic if isinstance(dic[k], basestring) or str(dic[k]).isdigit()}
        clean_dict.update({k: dic[k] for k in dic if isinstance(dic[k], float) and not isnan(dic[k])})
        if 'hashid' in clean_dict:
    	# print dic
        	a=Join(**clean_dict)
        	a.save()
        else: 
            print clean_dict

    return (1, difftime)
    # print df.head()
    # success=addtodatastore(df)
    # print df.head()
    # print "success"


        

def setbroker(page_id):
    a = Join.objects.get(hashid = page_id)
    b = Join.objects.filter(duplicategroupid = a.duplicategroupid)
    a.isbroker = not a.isbroker 
    a.save()
    if a.duplicategroupid==0: 
        return
    b = Join.objects.filter(duplicategroupid = a.duplicategroupid)
    for items in b: 
        items.isbroker = a.isbroker
        items.save()

def setscam(page_id):
    a = Join.objects.get(hashid = page_id)
    b = Join.objects.filter(duplicategroupid = a.duplicategroupid)
    a.isscam = not a.isscam
    a.save()
    if a.duplicategroupid==0: 
        return
    b = Join.objects.filter(duplicategroupid = a.duplicategroupid)
    for items in b: 
        items.isscam = a.isscam
        items.save()


def setemailsent(page_id):
    a = Join.objects.get(hashid = page_id)
    a.isemailsent = not a.isemailsent
    a.save()
    if a.duplicategroupid==0: 
        return
    b = Join.objects.filter(duplicategroupid = a.duplicategroupid)
    for items in b: 
        items.isemailsent = a.isemailsent
        items.save()
    

def updatelisting(data, page_id):
    clean_dict = {k: data[k] for k in data if len(data[k])>0}
    # clean_dict = data
    a = Join.objects.get(hashid = page_id)

    # print "This is the clean dict: ", clean_dict

    if 'listing_type_text' in clean_dict:
        a.listing_type_text = clean_dict['listing_type_text']
    if 'name' in clean_dict:
        a.name = clean_dict['name']
    if 'email' in clean_dict:
        a.email = clean_dict['email']
    if 'neighborhood' in clean_dict:
        a.neighborhood = clean_dict['neighborhood']
    if 'bedroom' in clean_dict:
        a.bedrooms = clean_dict['bedroom']
    if 'bathroom' in clean_dict:
        a.bathroom = clean_dict['bathroom']

    a.save()


def updateneighbcoordinates():
    exceptions = ['Manhattan Valley']
    neighborhods = Neighborhood.objects.all()
    f = False
    for n in neighborhods: 
        if n.area == 'Old Howard Beach':
            n.parentarea = 'Queens'
        if n.area == 'Howard Park':
            n.parentarea = 'Queens'
        if n.area == 'Manor Heights':
            n.parentarea = 'Staten Island'
        if n.area == 'Sandy Ground':
            n.parentarea = 'Staten Island'

        if n.latitude<41 and n.latitude>40 and n.longitude>-74.5 and n.longitude<-73 and n.updated: 
            continue
        #     continue
        n.updated = True 
        time.sleep(0.1)
        area = n.area
        parentarea = n.parentarea

        parentdict = {"East Shore": "Staten Island", 'South Shore': "Staten Island", 'North Shore': 'Staten Island'}

        namedict = {"Starrett City": "Pennsylvania Ave", "Fordham Bronx": "Fordham University Bronx", "Central Midtown": "Midtown",\
         "Northeastern Queens": "NorthEastern Cleaning Services Queens", "High Rock": "High Rock Park", "Fort Worth": "Fort Wadsworth",\
          "Arlington" : "Upper East Side", "Arlington Club" : "Upper East Side", "Clifton" : "Clifton House Owners Corporation", \
          "Livingston" :"Livingston Management Services" , "Ward Hill" : "Ward Avenue", "Sandy Ground" : "Korean War Vets Parkway", \
          "Brookville" : "Brookville  Park", "Howard Park" : "Howard Beach", "Emerson Hill" : "Emerson Hill Staten Island", "Manhattan Valley": "Upper West Side" }
        
        if area in namedict:
            area = namedict[area]

        dic = {"address": area + " " + parentarea + " New York"}
        url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(dic)
        try:
            response = urllib2.urlopen(url)
            data = json.load(response) 
            if "results" in data:
                lat = data["results"][0]["geometry"]['location']['lat']
                lng = data["results"][0]["geometry"]['location']['lng']

                # print dic['address'], lat, lng
                n.latitude = lat
                n.longitude = lng
                n.save()
            else: 
                dic = {"address": area + " " + parentarea + " NY"}
                url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(dic)
                try:
                    response = urllib2.urlopen(url)
                    data = json.load(response) 
                    if "results" in data:
                        lat = data["results"][0]["geometry"]['location']['lat']
                        lng = data["results"][0]["geometry"]['location']['lng']

                        # print dic['address'], lat, lng
                        n.latitude = lat
                        n.longitude = lng
                        n.save()

                except: 
                    # print "Again Error: ", n.area, n.parentarea
                    continue

        except: 
            print "Error:", n.area, n.parentarea
            continue




def updateneighbhashid():
    neighborhoods = Neighborhood.objects.all()
    maxlat = 41.
    minlat = 40.5
    maxlng = -73.7
    minlng = -74.3
    latlist = [n.latitude for n in neighborhoods]
    latlist = [max(minlat, min(maxlat, l)) for l in latlist]
    lnglist = [n.longitude for n in neighborhoods]
    lnglist = [max(minlng, min(maxlng, l)) for l in lnglist]
    arealist = [n.area for n in neighborhoods]

    ascilist = []
    for i in range(len(neighborhoods)):

        n = neighborhoods[i]
        a = n.area
        initials = [s[0] for s in a.split()]
        nid = '00' 
        nid = str(int(2*(sum([ord(s) for s in initials])-60))/10).zfill(2)[:2]
        latid = '000'
        latid = str(int(999.9*(latlist[i]-minlat)/(maxlat - minlat))).zfill(3)
        lonid = '000'
        lonid = str(int(999.9*(lnglist[i]-minlng)/(maxlng - minlng))).zfill(3)
        hid = int(nid + latid + lonid)
        n.hashid = hid
        n.save()


def updateneighbors():
    source = []
    areas = []
    nids = []
    parentareas = []
    boroughs = []

    '''
    url = "https://www.renthop.com/"
    html = call_agent(url)
    soup = BeautifulSoup(html, "html.parser")

    boroughsselector = soup.find("div", {'class': 'checkbox-label-selector'})
    boroughoptions = boroughsselector.find_all("div", {'class': 'tab-link-single'})
    for b in boroughoptions: 
        tempname = re.match(r'(.+)\s+\(.+', b.text.strip().replace('\n','')).group(1)
        print "The borough name is: ", tempname
        boroughs.append(tempname)

    print len(boroughs), boroughs

    for i in range(1,7):
        boroughname = boroughs[i-1]

        neigbcolumn = soup.find("div", {'id': 'neighborhood-column-%d'%i})
        neighgoups = neigbcolumn.find_all("div", {'class': 'neighborhood-group'})
        for g in neighgoups:
            section = g.find("div", {'class': 'neighborhood-group-item'})
            sectionname = section.text.strip().replace('\n','')
            areas.append(sectionname)
            parentareas.append(boroughname)
            nids.append(section.find("input")["id"])
            neighbors = g.find_all("div", {'class': 'neighborhood-single-item'})
            for n in neighbors: 
                label = n.find("label")
                areas.append(label.text.strip().replace('\n',''))
                nids.append(label["map_key"])
                parentareas.append(sectionname)

    for i in range(len(areas)):
        source.append('renthop')
        print areas[i], nids[i], parentareas[i]

    print len(source), len(areas), len(parentareas), len(nids)



    
    url = "http://streeteasy.com/rentals"
    html = call_agent(url)
    soup = BeautifulSoup(html, "html.parser")
    areaitems = soup.find("ul", {'class': "area-items"})
    indents=[]
    indents.append(areaitems.find_all("li", class_="item indent-0"))
    indents.append(areaitems.find_all("li", class_="item indent-1"))
    indents.append(areaitems.find_all("li", class_="item indent-2"))
    indents.append(areaitems.find_all("li", class_="item indent-3"))
    
    for i in indents[0]: 
        areas.append(i.find("label").text) 
        parentareas.append(None)
        nids.append(i.find("label")["for"])
        source.append("streeteasy")

            
    for j in range(1,4): 
        for i in indents[j]: 
            areas.append(i.find("label").text) 
            nids.append(i.find("label")["for"])
            parentid = "area-"+i.find("input")["data-parent-id"]
            parenttext = areaitems.find("label", {'for': parentid}).text
            parentareas.append(parenttext)
            source.append("streeteasy")


    # url = "http://www.nybits.com/search/"
    # html = call_agent(url)
    # soup = BeautifulSoup(html, "html.parser")
    
    # searchtable = soup.find("table",{"class":"searchformtable"})
    # zones = searchtable.find_all("div", {'class':'zonestosearchdiv'})
    
    # print len(zones)
    # for z in zones: 
    #     title = z.find("div", {'class': 'zonecheckbox'})
    #     borough = title.find("input")
    #     if borough:
    #         boroughlist = borough["onclick"]
    #         boroughtext = z.find("div", {'class': 'zonecheckbox'}).find("input").text
    #         subzonelist = z.find("div", {'class': 'subzonecheckboxes'}).find_all("input")
    #         subzonedict = {}
    #         for sub in subzonelist: 
    #             subzonedict[sub["value"]] = sub["value"].replace('_', ' ').title()
            
    #         neighbors = re.match(r'\w+\((.+)\)',boroughlist).group(1).replace("'", '').split(',')[2:]
    #         for n in neighbors: 
    #             areas.append(subzonedict[n].strip())
    #             parentareas.append(boroughtext.strip())
    #             nids.append(n)
    #             source.append("nybits")
    #     else:
    #         boroughlist = z.find("div", {'class': 'subzonecheckboxes'}).find_all("input")
    #         for b in boroughlist:
    #             value = b["value"]
    #             areas.append(value.replace('_', ' ').title())
    #             nids.append(value)
    #             parentareas.append(None)
    #             source.append("nybits")
                
    boroughdict = {"borough_1": "Manhattan", "borough_2": "Brooklyn", "borough_3": "Queens", "borough_4": "Bronx", "borough_5": "Staten Island"}              
    url = "http://www.nakedapartments.com/"
    html = call_agent(url)
    soup = BeautifulSoup(html, "html.parser")
    #print soup.prettify()
    boroughs = soup.find_all("div", {'class': 'boroughs'})
    for b in boroughs: 
        bid = b["id"]
        neighborhoods = b.find_all("div", {"class": "checkboxCont"})
        for n in neighborhoods:
            areas.append(n.text.strip())
            parentareas.append(boroughdict[bid])
            tempidstring = re.match(r'.*_(\d+)', n.find("label")["for"]).groups()
            nids.append(int(tempidstring[0]))
            source.append("nakedapartments")

  
    dfdict = []
    for i in range(len(areas)): 
        dfdict.append({"area": areas[i], 'parentarea': parentareas[i], 'nid': nids[i], 'source': source[i]})
    # dfdict = [d for d in dfdict if d
    for dic in dfdict: 
        existing = Neighborhood.objects.filter(source = dic['source'], nid = dic['nid'])
        existing.delete()

        clean_dict = {k: dic[k] for k in dic if dic[k]}
        a=Neighborhood(**clean_dict)
        try:
            a.save()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
    '''
    updateneighbcoordinates()
    updateneighbhashid()
    
    
def match_address(w, adrs): 
    adrs=adrs.lower()
    p=0.5
    # 2 is streeteasy, 3 is nybits, and 4 is nakedapartments
    neighbordata = Neighborhood.objects.filter(source = w)
    neighbNames=[n.area for n in neighbordata]
    nameDict={}
    for n in neighbNames:
        nameDict[n]=name_similarity(adrs, n)        

    sortedNeighbs=sorted(neighbNames, key=lambda x: nameDict[x], reverse=True) 

    if sortedNeighbs: 
        # print w, adrs, sortedNeighbs[0:5], [nameDict[x] for x in sortedNeighbs[0:5]]
    #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
        theneighbor = neighbordata.filter(area = sortedNeighbs[0]) 
        if nameDict[sortedNeighbs[0]]>p and theneighbor:
            return (theneighbor[0].parentarea,theneighbor[0].area,theneighbor[0].nid)
        else: 
            return (-1,-1,-1)
    else: 
        return (-1,-1,-1)

def matchallneighbor(adrs): 
    adrs=adrs.lower()
    p=0.5
    # 2 is streeteasy, 3 is nybits, and 4 is nakedapartments
    # print adrs
    neighbordata = Neighborhood.objects.all()
    neighbNames=set([n.area for n in neighbordata]) 
    nameDict={}
    for n in neighbNames:
        nameDict[n]=name_similarity(adrs, n)  

    sortedNeighbs=sorted(neighbNames, key=lambda x: nameDict[x], reverse=True) 
    if sortedNeighbs: 
        # print adrs, sortedNeighbs[0:5], [nameDict[x] for x in sortedNeighbs[0:5]]
    #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
        theneighbor = neighbordata.filter(area = sortedNeighbs[0])
        print nameDict[sortedNeighbs[0]]
        if nameDict[sortedNeighbs[0]]>p:
            return (theneighbor[0].hashid, theneighbor[0].parentarea, theneighbor[0].area) 
        else: 
            return (None,None,None)
    else: 
        return (None,None,None)


def retrieve_hidden(w, soup, getVars):
    if w == 'nybits':
        form=soup.find('form', {'name':'sform'})
        input_hidden_values=form.find_all('input', {'type':'hidden'})
        for inp in input_hidden_values: 
            getVars[inp.get('name')]= inp.get('value')
    
    return getVars
    

def retrieve_beds(w, getVars, beds): 
    if beds is int: 
        beds=min(beds, 4)
    beds = str(beds)
    if w == 'streeteasy':
        getVars["beds"] = beds
    # elif w == 'nybits': 
    #     dic = {1:"1br", 2:"2br", "loft":"loft", 3:"3more", 4:"3more", "studio":"studio"}
    #     getVars["!!atypes"] =  dic[beds]
    elif w == 'nakedapartments': 
        nakeddict={'0':"1", "studio":"1", '1':"3", '2':"4", '3':'5', '4':"6", "room":"11", "loft": "2"}
        getVars["aids"]=nakeddict[beds]

    elif w == 'renthop':
        dic = {'loft': '-2', 'studio': '0', 'room': '-1', '1':'1', '2':'2', '3':'3', '4':'4'}
        # print "The beds are:", beds 
        getVars["bedrooms[]"] = dic[beds]
    
    # if w == 'nybits': 
    #     getVars["bedrooms"]=beds
        
    return getVars

def retrieve_baths(w, getVars, baths): 
    if baths:
        if w == 'nybits': 
            getVars["baths"]=round(baths)
        elif w == 'nakedapartments':
            getVars["bathrooms"]=int(baths)
        elif w == 'renthop':
            getVars["bathrooms[]"]= int(baths)

    return getVars
    
def retrieve_address(w, address, getVars): 
    if w=='nybits':
        m=match_address(w, address)
        if m[0]:
            getVars["!!nsearch"]=m[1]
        else:
            getVars["!!bsearch"]=m[1]
    
    elif w == 'nakedapartments':
        m=match_address(w, address)
        # print "The matched address for Nakedapartment is:", m
        if m[2]>0:
            getVars["nids"]=m[2]

    elif w == 'renthop':
        m=match_address(w, address)
        if m[2]>0:
            getVars["neighborhoods_str"]=m[2]

    
    # elif w == 'nakedapartments': 
    #     m=match_address(w, address)
    #     if m[2]::
    #         getVars["query"]=m[2]
        
    return getVars

def retrieve_price(w, getVars, pricemin, pricemax):
    # if w == 'nybits':
    #     form=soup.find('select', {'name':'!!rmin'})
    #     options=form.find_all('option')
    #     minprices=['0']
    #     for inp in options: 
    #         minprices.append(inp.get('value'))

    #     minprices=[int(p) for p in minprices if p.isdigit()]
    #     minp=min(minprices, key=lambda x:abs(x-pricemin))
    #     getVars['!!rmin']=minp

    #     form=soup.find('select', {'name':'!!rmax'})
    #     options=form.find_all('option')
    #     maxprices=[]
    #     for inp in options: 
    #         maxprices.append(inp.get('value'))

    #     maxprices=[int(p) for p in maxprices if p.isdigit()]
    #     maxp=min(maxprices, key=lambda x:abs(x-pricemax))
    #     getVars['!!rmax']=maxp
    
    if w == 'nakedapartments': 
        getVars['min_rent']=pricemin
        getVars['max_rent']=pricemax
    elif w == 'renthop':
        getVars['min_price']=pricemin
        getVars['max_price']=pricemax
    # elif w==5:
    #     getVars['min_price']=pricemin
    #     getVars['max_price']=pricemax      

    return getVars

def retrieve_fee(w, getVars): 
    if w == 'nybits': 
        getVars["fee"] = "nofee"
        
    return getVars


def currentdatetimestring():
    dt = datetime.datetime.now()
    return "%s-%s-%s %s:%s"%(str(dt.year), str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))


def calhashid(inbeds, inneighborhood, inaddress, inprice, insource, intype='1'): 
# beds is a string, price is a integer number and source is a string 
    sourcenum = {'joinery':1, 'streeteasy': 2, 'nybits': 3, 'nakedapartments':4, 'craigslist': 6, 'renthop':5, 'zumper': 7, 'nooklyn': 8}
    bedsdict = {'studio': '8', 'loft': '9'}

    ##############################
    sid=str(sourcenum[insource])

    if inbeds:
        beds = str(inbeds)
        if beds.isdigit():
            sid += beds.zfill(1)[:1]
        else: 
            sid += bedsdict[beds]
    else:
        sid += '0'
    
    nlength = 0
    nparts = 0
    naddress = 0
    vaddress = 0

    if inneighborhood:
        neighborhood = inneighborhood.strip()
        nlength = len(neighborhood)
        nparts = len(neighborhood.split())
    
    if inaddress:
        address = inaddress.strip()
        naddress = len(address)
        tempunit = re.match(r'[^\d]*(\d+)[^\d]*.*', address)
        vaddress = int(tempunit.group(1)) if tempunit else 0

        
    temptext='0000'
    if nlength > 0: 
        initials = [s[0] for s in neighborhood.split()]
        temp=sum([ord(s) for s in initials])
        temptext = str(nlength+nparts+naddress+vaddress+temp).zfill(4)[:4]
    elif inaddress:
        temptext = str(naddress).zfill(4)[:4]

    sid+=temptext
        
    
    if isinstance(inprice,float) or (inprice is None):
        sid+='00'
    else: 
        sid += str(int(round(inprice/100.))).zfill(2)[:2]

    if intype and (intype == 'room'):
        sid +='0'
    else: 
        sid += '1'
    
    # print temptext, price, naddress, nlength, sid
    return int(sid)


def updatehashids(): 
    temp = Join.objects.all() 
    sourcenum = {'joinery':1, 'streeteasy': 2, 'nybits': 3, 'nakedapartments':4, 'craigslist': 6, 'renthop':5}
    difflist = []
    for e in temp: 
        tempbedroom = e.bedrooms
        tempbathroom = e.bathrooms 
        tempprice = e.price
        tempaddress = e.full_address
        tempneighborhood = e.neighborhood
        tempsource = e.source
        temptype = e.listing_type_text

    # print sn
        HID = calhashid(tempbedroom, tempneighborhood, tempaddress, tempprice, tempsource, temptype)

        # neighbidhashid = findneighbhashid(tempneighborhood)
        # hashid = str(neighbidhashid).zfill(8)[:8] if neighbidhashid>0 else '0'.zfill(8)

        # # print "This is the hashcode: ", nh
        # price = '0000'
        # beds = '0'
        # baths = '0'
        # apt = '1'
        # source = '0'

        # if tempprice:
        #     price = str(int(tempprice/10)).zfill(4)[:4]

        # if tempbedroom: 
        #     tb = str(tempbedroom)
        #     if tb.isdigit():
        #         beds = str(int(min(tb, '7')))
        #     else: 
        #         if tb =='studio':
        #             beds = '8'
        #         elif tb == 'loft':
        #             beds = '9'
        # if temptype and temptype == 'room': 
        #     apt = '0'

        # if tempsource: 
        #     source = str(sourcenum[tempsource])

        # HID = int(source+hashid+price+beds+baths+apt)
        oldhash = e.hashid
        e.hashid = HID
        if oldhash != HID:
            print oldhash, HID
            difflist.append(True)
        try:
            e.save()
        except: 
            print "I cannot change it on db"

        # print "The new hashid of the listing will be: ", Join.objects.get(hashid = HID).hashid 

    print "The number of changed on db are:", len(difflist)

def insert2db(dfdict):
    # print "The length of dict is :", len(dfdict)
    hashidlist = [d['hashid'] for d in dfdict]
    N = len(dfdict)
    # print "The unique number of hashids:", set(hashidlist)
    hash2dblist = []
    for dic in dfdict: 
        if len(Join.objects.filter(hashid = dic['hashid']))>0:
            # print "Hashid:", dic["hashid"]
            hashidlist.remove(dic['hashid'])
            a = Join.objects.filter(hashid = dic['hashid'])
            dic['created_at'] = max(a[0].created_at, dic['created_at']) if ("created_at" in dic) else a[0].created_at
            if 'views' in dic: 
                dic['views'] = max(a[0].views, dic['views'])

            a.delete()

        clean_dict = {k: dic[k] for k in dic if isinstance(dic[k], basestring) or str(dic[k]).isdigit()}
        clean_dict.update({k: dic[k] for k in dic if isinstance(dic[k], float) and not isnan(dic[k])})
        # print clean_dict
        if 'hashid' in clean_dict:
        # print dic
            a=Join(**clean_dict)
            try:
                a.save()
                hash2dblist.append(clean_dict["hashid"])
                # return (hashidlist, N)
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
        else: 
            print "No hashid: ", clean_dict

    # print hash2dblist
    # print hash2dblist[0]
    return (hash2dblist, N)

def updatebedsbaths(title): 
    beds = None
    baths = None
    if title: 
        title = re.sub('\s+', ' ', title.lower())
    else: 
        return (beds, baths)

    tempbeds = re.match(r'.*(\d+)\s*bed.*', title)
    tempbeds = re.match(r'.*(\d)br.*', title) if not tempbeds else tempbeds
    tempbeds = re.match(r'.*(\d+)br(\s.*|,).*', title) if not tempbeds else tempbeds
    if not tempbeds:
        if 'studio' in title: 
            beds = 'studio'
        elif 'loft' in title: 
            beds = 'loft'
    else:
        beds = tempbeds.group(1) if tempbeds else None

    tempbath = re.match(r'.*(\d?.?\d)\s*bath.*', title)
    tempbath = re.match(r'.*(\d?.?\d)ba.*', title) if not tempbath else tempbath
    tempbath = re.match(r'.*(\d?.?\d)ba(\s.*|,).*', title) if not tempbath else tempbath
    baths = tempbath.group(1) if tempbath else None

    return (beds, baths)


def url2db(urls): 
    sourcedict = {'http://www.nakedapartments.com/': 'nakedapartments' , 'http://www.nybits.com/': 'nybits',  'http://streeteasy.com/': 'streeteasy', 'https://www.renthop.com/': 'renthop'}
    dfdict = [] # the array of dictionaries 
    # urls = ['http://www.nakedapartments.com/renter/listings/search?max_rent=6021&min_rent=1764&bathrooms=1', 'https://www.renthop.com/search/nyc?bedrooms%5B%5D=2&bathrooms%5B%5D=1&features=No%2BFee&neighborhoods_str=111&min_price=1896&max_price=2940']
    # urls = ['https://www.renthop.com/search/nyc?bedrooms%5B%5D=0&bathrooms%5B%5D=1&min_price=1018&features=No%2BFee&max_price=2775']
    # urls = ['http://streeteasy.com/for-rent/Norwood/price:1577-4283%7Cno_fee:0%7Cbeds=2']#, 'http://www.nakedapartments.com/renter/listings/search?nids=198&max_rent=4283&min_rent=1577&bathrooms=1', 'https://www.renthop.com/search/nyc?bedrooms%5B%5D=2&bathrooms%5B%5D=1&features=No%2BFee&neighborhoods_str=113&min_price=1577&max_price=4283']
    # urls = ['https://www.renthop.com/search/nyc?bedrooms%5B%5D=3&max_price=2500&features=No%2BFee&min_price=2000&neighborhoods_str=41']
    updatehashlist = []
    attributes = dict.fromkeys(['hashid', 'title', 'bedrooms', 'bathrooms', 'neighborhood', 'ft2', 'price', 'full_address', 'image_url', 'url', 'parent_neighborhood', 'source', 'created_at', 'score'], None)
    attributelist = {}

    for a in attributes: 
        attributelist[a] = []
    # attributelist = dict.fromkeys(attributes.keys(), [])
    print "The length of attribute list : ", len(attributelist)
    for url in urls:
        checktime()
        baseURL = re.match(r'\w+://(.+\.\w+)/', url).group(0)
        if baseURL not in sourcedict:
            return False

        print url 
        soup = call_agent(url)
        w = sourcedict[baseURL]

        # print baseURL, w
        if w == 'streeteasy':
            rows = soup.findAll("div", {"class":'item'})
            print "Streeteasy, The lenght of results are:", len(rows)
            for a in attributes: 
                attributelist[a] = []
            for row in rows: 
                try:
                    attributes = dict.fromkeys(attributes, None)
                    attributes['url'] = baseURL+row.find("div", {"class": "details-title"}).find("a")["href"]
                    tempprice = re.match(r'\$(\d+),(\d{3})', row.find("span", {"class": "price"}).text)
                    attributes['price']  = int(tempprice.group(1)+tempprice.group(2)) if tempprice else None 
                    # print "The price is:", attributes['price']
                    tempimage = row.find(attrs = {"class": "lazy"})
                    attributes['image_url']  = tempimage["data-original"] if tempimage else None
                    # print "The image is done"
                    t = row.find(attrs = {"class": "details-title"}).find("a")
                    t = t.text if t else None
                    # print t 
                    attributes['title'] = t
                    attributes['full_address']  = (t.split('#')[0].strip() if '#' in t else t) if t else None
                    # print  attributes['full_address']
                    details = row.findAll(attrs = {"class":  'details_info'})
                    if details:
                        for d in details:
                            text = re.sub('\s+', ' ', d.text)
                            if any(x in text for x in ['bed', 'bath', 'loft', 'studio']):
                                attributes['title'] += ' '+ text
                            # print d.text.strip()
                            sep = ' in '
                            rest = text.split(sep,1)[0]
                            #print 'This is the split: ',rest
                            rest = rest.strip()
                            neighb = re.match(r'.+%s in (.*)' % (rest), text)
                            filters = ['Open House','Listed', 'Building', 'Rental Unit', 'Multi-family']
                            filterBool = not any(s in rest for s in filters)
                            attributes['neighborhood']  = neighb.group(1) if neighb else attributes['neighborhood']
                            # print "The neighborhood: ", attributes['neighborhood']
                            tempbeds = re.match(r'.*(\d+)\s*bed.*', text)
                            attributes['bedrooms']  = tempbeds.group(1) if tempbeds else attributes['bedrooms'] 
                            # print "The number of bedrooms: ", attributes['bedrooms']
                            tempbath = re.match(r'.*(\d+)\s*bath.*', text)
                            attributes['bathrooms']  = tempbath.group(1) if tempbath else attributes['bathrooms']
                            # print "The number of bathrooms :", attributes['bathrooms']
                            tempft2 = re.match(r'.*(\d+)\s*ft.*', text)
                            attributes['ft2']  = tempft2.group(1) if tempft2 else attributes['ft2']
                            # print "The ft2 size is:", attributes['ft2']
                    # neighbtext = re.sub('\s+', ' ', details[1].text)
                    # neighb = re.match(r'.+Rental Unit in (.*)', neighbtext)
                    # if neighb: 
                    #     temp = neighb.groups(1)[0]        
                    #     neighborhoods.append(temp)
                    # else:
                    #     neighborhoods.append('')
                    print attributes['bedrooms'], attributes['bathrooms'], updatebedsbaths(attributes['title'])
                    # if details:
                    #     sizeinfo = details[0].text
                    #     print "The size info text is:", sizeinfo
                    #     tempbeds = re.match(r'.*(\d+)\s*bed.*', sizeinfo)
                    #     beds.append(tempbeds.group(1) if tempbeds else None)
                    #     tempbath = re.match(r'.*(\d+)\s*bath.*', sizeinfo)
                    #     baths.append(tempbath.group(1) if tempbath else None)
                    #     tempft2 = re.match(r'.*(\d+)\s*ft.*', sizeinfo)
                    #     ft2s.append(tempft2.group(1) if tempft2 else None)

                    # print "Neighborhood:", neighborhoods[-1]

                    attributes['source'] = w
                    SID = calhashid(attributes['bedrooms'], attributes['neighborhood'], attributes['full_address'], attributes['price'], w)
                    # print SID
                    DT = currentdatetimestring()
                    # print DT
                    attributes['hashid']  = SID
                    attributes['created_at']  = DT
                    # print DT
                    areaname = None
                    if attributes['neighborhood']:
                        # print "neighborhood:", neighborhoods[-1]
                        areaname = match_address(w, attributes['neighborhood'])
                        # print "The matching area name is :", areaname
                        if areaname:
                            attributes['neighborhood'] = areaname[1]
                            attributes['parent_neighborhood']  = areaname[0]
                    else:
                        print "non neighborhood"
                        attributes['parent_neighborhood']  = None 

                    
                    for k in attributes: 
                        attributelist[k].append(attributes[k])
                    # newdic = {'hashid': hashid,'full_address': address, 'bedrooms':beds, 'price': price, 'bathrooms': baths, 'image_url': imagelink, 'neighborhood': neighborhood, 'parent_neighborhood': parent_neighborhood, 'url': urllink, 'source': w, 'created_at': created_at}
                    newdic = attributes
                    newhash, n = insert2db([newdic])
                    # print newhash, n
                    dfdict.append(newdic)
                    updatehashlist.append(newhash[0])

                except:
                    print "Problem with the row"
                    continue

            print w, 
            for k in attributelist: 
                print len(attributelist[k]),
            print '\n'


            # print "After streeteasy:", len(prices), len(baths)


        # elif w == 'nybits':
        #     table = soup.find("table", {"id": "rentaltable"})
        #     rows = table.findAll("tr")

        #     tempaddresses = []
        #     tempimagelinks = []
        #     tempprices = []
        #     tempbeds = []
        #     tempneighborhood = []
        #     tempbedroom = []
        #     tempurllinks = []
        #     n = 3
        #     i=0
        #     for row in rows:
        #         if i>=n: 
        #             break
        #         firtcolumn = row.find("td", {"class": "lst_sr_price"})
        #         if (not firtcolumn) or (len(firtcolumn.text)==0): 
        #             continue
        #         secondcolumn = row.find("td", {"class": "lst_sr_topcell"})
        #         if not secondcolumn:
        #             continue
        #         featureimage = secondcolumn.find("img")
        #     #     print featureimage
        #         if featureimage: 
        #             i+=1
        #             url = secondcolumn.find("a")["href"]
        #             tempurllinks.append(url)
        #             pricetext =  firtcolumn.text.replace('\n', '')
        #             # print "this is the first column: ", pricetext
        #             pricestring = re.match(r'.*\$(\d+),(\d{3})', pricetext) 
        #             tempprices.append(int(pricestring.group(1)+pricestring.group(2)))
        #             html = call_agent(url)
        #             soup = BeautifulSoup(html, "html.parser")
        #             title = soup.find("div", {"id": "dancefloor"}).find('h1').text
        #             bedroom = re.match(r'(\d).Bedroom', title).group(1)
        #             tempbedroom.append(int(bedroom))



        #             content = soup.find("div", {"class": "listing_content"})
        #             tempimagelinks.append(content.find("img")["src"])
        #             table = soup.find("table", {"class": "listing_summary"})
        #             rows = table.findAll("tr")
        #             for row in rows: 
        #                 columns = row.findAll("td")
        #                 if "Building" in columns[0].text:
        #                     tempaddresses.append(columns[1].text.replace('\n', ''))
        #                     continue
        #                 elif "Neighborhood" in columns[0].text:
        #                     tempneighb = columns[1].text.replace('\n', '')
        #                     neigb = tempneighb.split(';')[-1]
        #                     tempneighborhood.append(neigb)
                    

        #             SID = calhashid(tempbedroom[-1], tempneighborhood[-1], tempaddresses[-1], tempprices[-1], w)
        #             DT = currentdatetimestring()
        #             hashids.append(SID)
        #             created_at.append(DT)
        #             baths.append(None)
        #             ft2s.append(None)
        #             sourcepages.append(w)

        #     prices += tempprices
        #     addresses += tempaddresses
        #     neighborhoods += tempneighborhood
        #     imagelinks += tempimagelinks
        #     urllinks += tempurllinks
        #     beds += tempbedroom



        elif w == 'nakedapartments':
            content = soup.find("div", {'class': "listing-results b"})

            # firstrow = content.find("div", {'class': 'listing-row listing-row-standard  mappable-element ab-test mobile-web-style row'})
            rows = content.findAll("div", {'class' : "listing-row listing-row-standard featured mappable-element row"}) 
            # print w, " The length of rows: ", len(rows)
            for a in attributes: 
                attributelist[a] = []
            for row in rows: 
                try:
                    attributes = dict.fromkeys(attributes, None)
                    # print row.prettify()
                    sections = row.findAll("div")
                    listingtitle = None
                    for sec in sections: 
                        # print sec.prettify()
                        if sec.has_attr("class"): 
                            if "listing-image" in sec["class"]: 
                                listingemage = sec
                                rowimage = listingemage.find('img', {"class": "lazy"})
                                attributes['image_url'] = rowimage['src'] if rowimage else attributes['image_url']
                                # print imagelinks[-1]
                            elif "listing-details" in sec["class"]: 
                                rowinfo = sec 
                                listingtitle = rowinfo.find(attrs={"class": "listing-title"})
                                attributes['title'] = listingtitle.text if listingtitle else None

                    # print listingemage.prettify()                
                    # print rowimage.prettify()                
                #     print "imagelink:", rowimage["data-original"]
                    # rowinfo = row.find(attrs={'class': re.compile(r"listing-details col-xs-\d+")})
                    # print getframeinfo(currentframe()).lineno, rowinfo.prettify()
                    # print "Row info is:", rowin
                    # print getframeinfo(currentframe()).lineno 
                    if not listingtitle: 
                        continue 

                    tempprice = re.match(r'\$(\d+),(\d{3})', listingtitle.text)
                    # print tempprice
                    attributes['price'] = int(tempprice.group(1)+tempprice.group(2)) if tempprice else None
                    # print getframeinfo(currentframe()).lineno 

                    attributes['url'] = listingtitle['href']
                    listingaddress = rowinfo.find(attrs={"class": "listing-address"})
                    attributes['full_address'] = listingaddress.text if listingaddress else None
                    # print getframeinfo(currentframe()).lineno 

                    sizeinfo = rowinfo.find("div", {"class": "listing-size"})
                    # print sizeinfo
                    if sizeinfo: 
                        sizeinfo = re.sub('\s+', ' ', sizeinfo.text).lower()
                        attributes['title'] = (attributes['title']+ ' ' + sizeinfo) if attributes['title'] else sizeinfo
                        tempbeds = re.match(r'.*(\d)br.*', sizeinfo) 
                        # print sizeinfo
                        if 'studio' in sizeinfo: 
                            attributes['bedrooms'] = 'studio'
                        elif 'loft' in sizeinfo: 
                            attributes['bedrooms'] = 'loft'
                        else:
                            attributes['bedrooms'] = tempbeds.group(1) if tempbeds else None

                        # print "The nubmer of bedrooms: ", attributes['bedrooms']
                        tempbath = re.match(r'.*(\d?.?\d)ba.*', sizeinfo.lower())
                        attributes['bathrooms'] = tempbath.group(1) if tempbath else None
                        # print "The number of bathrooms: ",  attributes['bathrooms']

                        # bedsbaths = re.match(r'(\d)br, (\d?.?\d)ba', sizeinfo.lower())

                    # print getframeinfo(currentframe()).lineno,listingaddress.text
                    listingneighb = rowinfo.find(attrs = {"class": "listing-neighborhood"})
                    # print getframeinfo(currentframe()).lineno, listingneighb.text
                    attributes['neighborhood'] = listingneighb.text if listingneighb else None
                    # print getframeinfo(currentframe()).lineno
                    attributes['source'] = w
                    #beds, neighborhood, address, price, source,
                    SID = calhashid(attributes['bedrooms'], attributes['neighborhood'], attributes['full_address'], attributes['price'], w)
                    # print getframeinfo(currentframe()).lineno, SID
                    DT = currentdatetimestring()
                    attributes['hashid'] = SID
                    # print getframeinfo(currentframe()).lineno, DT
                    # created_at.append(DT)
                    attributes['created_at'] = DT
                    if attributes['neighborhood']:
                        areaname = match_address(w, attributes['neighborhood'])
                        if areaname:
                            attributes['neighborhood'] = areaname[1]
                            attributes['parent_neighborhood'] = areaname[0]
                    # print "The matching area name is :", areaname
                    newdic = attributes
                    # print w, "Dict : ", newdic
                    newhash, n = insert2db([newdic])
                    dfdict.append(newdic)
                    updatehashlist.append(newhash[0])
                    print attributes['bedrooms'], attributes['bathrooms'], updatebedsbaths(attributes['title'])
                    for k in attributes: 
                        attributelist[k].append(attributes[k])
                except:
                    continue

            print w, 
            for k in attributelist: 
                print len(attributelist[k]),
            print '\n'



            # print "After nakedapartments: ", len(prices), len(baths)
        elif w == 'renthop':
            rows = soup.find_all("div", {"class": "search-listing"})
            print " The length of rows are: ", len(rows)
            for a in attributes: 
                attributelist[a] = []
            # print attributelist
            for row in rows: 
                try:
                    # print "The new row"
                    attributes = dict.fromkeys(attributes, None)
                    # print "New Row"
                    imagelinks = []
                    photolayout = row.find("a", {'class': "search-photo-layout"})
                    photolist = photolayout.find_all("div")
                    imagesection = photolist[0].find("img")
                    if not imagesection: 
                        continue
                    attributes['image_url'] = imagesection["src"]
                    if len(photolist)>1:
                        secondimagestring = photolist[1]["style"]
                        simagegroup = re.match(r'.+url\((.+)\)', secondimagestring)
                        if simagegroup: 
                            attributes['image_url'] = simagegroup.group(1) 

                    temptitle = row.find("div", {'class': "font-size-100 bold listing-search-text"})
                    # print temptitle.text
                    titlestring = temptitle.text.replace('\n', '').strip()
                    attributes['title'] = titlestring

                    attributes['url'] = temptitle.find("a")["href"]
                    bedsbaths = re.match(r'(\d)br, (\d?.?\d)ba.*', titlestring.lower())
                    tempbeds = re.match(r'.*(\d+)br(\s.*|,).*', titlestring.lower())
                    tempbath = re.match(r'.*(\d+)ba(\s.*|,).*', titlestring.lower())
                    # print "The bedroom string: ",  titlestring
                    attributes['bedrooms'] = int(tempbeds.group(1)) if tempbeds else None
                    if not attributes['bedrooms']:
                        attributes['bedrooms'] = 'loft' if 'loft' in titlestring.lower() else None
                        attributes['bedrooms'] = 'studio' if 'studio' in titlestring.lower() else attributes['bedrooms']

                    # print "The number of bedrooms: ", attributes['bedrooms']
                    attributes['bathrooms'] = int(tempbath.group(1)) if tempbath else None
                    # print "The bathrooms: ", 
                    # print beds[-1], baths[-1]
                    # print "The temporary title is : ", titlestring
                    addresgroup = re.match(r'.+at\s+(.+)', titlestring)
                    attributes['full_address'] = addresgroup.group(1) if addresgroup else None
                    # print attributes['full_address']
                    # print addresses[-1]

                    neighbstring = row.find("div", {'class': "font-size-80 listing-search-text"}).text.replace('\n', '').strip()
                    attributes['neighborhood'] = re.match(r'^(.+?)($|,)', neighbstring).group(1)
                    # print attributes['neighborhood']
                    # print neighborhoods[-1]
                    pricestr = row.find("div", {'class':  "bold color-fg-green font-size-100"}).text.replace('\n','').strip()

                    # print "The pricestring is :", pricestr

                    tempprice = re.match(r'\$(\d+),(\d{3}).*', pricestr)
                    attributes['price'] = int(tempprice.group(1)+tempprice.group(2))
                    # print attributes['price']
                    scorestr = row.find("div", {'class': "color-fg-blue hopscore-link bold font-size-100"})
                    attributes['score'] = int(scorestr["rs"]) if scorestr else None
                    # print attributes['score']
                    # print [len(s) for s in [beds, neighborhoods, addresses, prices]]
                    SID = calhashid(attributes['bedrooms'], attributes['neighborhood'], attributes['full_address'], attributes['price'], w)
                    DT = currentdatetimestring()
                    attributes['hashid'] =  SID
                    attributes['created_at'] = DT
                    # created_at.append(DT)
                    # sourcepages.append(w)
                    attributes['source'] = w
                    # print attributes['source']
                    if attributes['neighborhood']:
                        areaname = match_address(w, attributes['neighborhood'])
                        if areaname:
                            attributes['neighborhood'] = areaname[1]
                            attributes['parent_neighborhood'] = areaname[0]
                    # print "The matching area name is :", areaname
                    # print attributes['parent_neighborhood']
                    newdic = attributes
                    # print w, "Dict : ", newdic

                    newhash, n = insert2db([newdic])
                    dfdict.append(newdic)
                    updatehashlist.append(newhash[0])
                    print attributes['bedrooms'], attributes['bathrooms'], updatebedsbaths(attributes['title'])
                    # print "Length of attributes: ", attributes.keys()
                    for k in attributes.keys(): 
                        # print k, attributes[k],len(attributelist[k])
                        # print k
                        # print attributes['score'], attributelist['score']
                        attributelist[k].append(attributes[k])
                except:
                    continue

                    # print k

            print w, 
            for k in attributelist: 
                print len(attributelist[k]),
            print '\n'

        # for i in range(N):
        #     dfdict.append({'hashid': hashids[i],'full_address': addresses[i], 'bedroom':beds[i], 'price': prices[i], 'bathroom': baths[i], 'image_url': imagelinks[i], 'neighborhood': neighborhoods[i], 'linkurl': urllinks[i], 'source': sourcepages[i], 'created_at': created_at[i]})
        # # finaldict = {'hashid': hashids,'full_address': addresses, 'bedroom':beds, 'price': prices, 'bathroom': baths, 'image_url': imagelinks, 'neighborhood': neighborhoods, 'linkurl': urllinks, 'source': sourcepages, 'created_at': created_at}
    # df = pd.DataFrame(finaldict)
    # print df.head()
    # dfdict = df.to_dict(orient='records')
    # dfdict = [d for d in dfdict if d
    # print updatehashlist, len(dfdict)
    return (updatehashlist, len(dfdict))
    # return insert2db(dfdict)
def checktime():
    print 'checking time'
    return
    # if ...
    #     returnhashlist = codes.findlisting(data)
    #     resdict = {}
    #     for i in range(len(returnhashlist)):
    #         resdict[i] = returnhashlist[i]

    #     print resdict
    #pass

def create_url(address, pricemin=0, pricemax=20000, beds='1', baths=1, fee=0):
    urls = []
    sources = ['streeteasy', 'nakedapartments', 'renthop']

    for w in sources:
        checktime()
        if w == 'streeteasy':
            print 'streeteasy'
            m=match_address(w, address)
            # print "The result of math address streeteasy:", m
            if m[0]>0: 
                urladdress="http://streeteasy.com/for-rent/"+m[1].replace(' ', '-')
            else:
                urladdress="http://streeteasy.com/for-rent/nyc"
                
            urladdress=urladdress+"/price:%s-%s"%(pricemin, pricemax)
            urladdress=urladdress+"%7"+"Cno_fee:%d"%fee
            urladdress=urladdress+"%7"+"Cbeds:%s"%beds

            urls.append(urladdress)
        
        # elif w == 'nybits':
        #     url="http://www.nybits.com/search/"
        #     # filename=re.search("://.+\.\w+/", url).group(0).replace('.','_')[3:-1]#.replace(':','').replace('/','')
        #     #save_html(url, filename)
        #     # filepwd="Files/%s.html"%filename
        #     # html=codecs.open(filepwd)
        #     html = call_agent(url)
        #     soup = BeautifulSoup(html, "html.parser")
        #     getVars={'orderby':'dateposted'}
        #     getVars=retrieve_hidden(w, soup, getVars)
        #     getVars=retrieve_beds(w, getVars, beds)
        #     if address != 'nyc':
        #         getVars=retrieve_address(w, address, getVars)

        #     getVars=retrieve_price(w, soup, getVars, pricemin, pricemax)
        #     getVars = retrieve_fee(w, getVars)
        #     print "This is the nybits variables:", getVars
        #     urls.append(url + "?"+urllib.urlencode(getVars))
        
        elif w == 'nakedapartments':
            url="http://www.nakedapartments.com/"
            #save_html(url, filename)
    #         retrieve_neighborhoods(w, soup, 'www_nakedapartments_com', 'neighborhood_nakedapartments')
            getVars={}
            getVars=retrieve_beds(w, getVars, beds)
            if address != 'nyc':
                getVars=retrieve_address(w, address, getVars)
            else: 
                continue 

            getVars=retrieve_baths(w, getVars, baths )
            getVars=retrieve_price(w, getVars, pricemin, pricemax)
            # print "The result of address nakedapartments: ", getVars
            urls.append(url + "renter/listings/search?"+urllib.urlencode(getVars))

        elif w == 'renthop':
            url = "https://www.renthop.com/search/nyc?"
            getVars={'features': "No+Fee"}
            getVars=retrieve_beds(w, getVars, beds)
            getVars = retrieve_baths(w,getVars, baths)
            getVars = retrieve_price(w, getVars, pricemin, pricemax)
            if address != 'nyc':
                getVars=retrieve_address(w, address, getVars)

            urls.append(url + urllib.urlencode(getVars))
            print urls
    result = url2db(urls)
    print "The found results are: ", result
    return result


def sendrequesttoanni(tag):
    import requests
    dic = {}
    url = "https://elegant-chaise-69014.herokuapp.com/search/"
    #url = "http://localhost:8000/search/"
    # url = "https://mighty-shelf-86819.herokuapp.com/test/"
    print "this is the tag: ", tag
    # print "The tag is"
    if tag in ['search', 'alertrequest']:
        # url = "http://localhost:8000/search/"
        userid = random.choice(range(4))
        db = Neighborhood.objects.all()
        neighborhoods = [d.area for d in db]
        bedroom = random.choice(['studio', '1', '2', '3', "loft"])
        neibpick = random.choice(neighborhoods)
        minprice = int(1000+1000*random.random()) 
        maxprice = int(4000*random.random()+1000+minprice)
        dic = {'tag': tag, 'userid': userid, 'neighborhood': neibpick, 'minprice': minprice, 'maxprice': maxprice, 'bedrooms': bedroom}
        # dic ['minprice'] = 2000
        # dic ['maxprice'] = 2500
        # dic ['neighborhood'] = 'williamsburg'


    if tag == 'find': 
        url = "http://localhost:8000/find/"
        userid = random.choice(range(4))
        db = Join.objects.all()
        neighborhoods = [d.neighborhood for d in db]
        neibpick = random.choice(neighborhoods)

        bedroomlist = [d.bedrooms for d in db if d.bedrooms and (d.neighborhood==neibpick)]
        if len(bedroomlist) == 0: 
            bedroomlist.append(None)

        print "The bedroom list is:", bedroomlist
        bedroom = random.choice(bedroomlist)


        # minprice = int(1000*random.random()) 
        minprice = 0
        maxprice = 2*int(4000*random.random()+2000+minprice)
        dic = {'tag': tag, 'userid': userid, 'neighborhood': neibpick, 'minprice': minprice, 'maxprice': maxprice, 'bedrooms': bedroom}
        return dic


    elif tag == 'alert':
        # url = "http://localhost:8000/search/"
        userid = random.choice(range(4))
        db = Join.objects.all() 
        hashids = [n.hashid for n in db] 
        # nitems = random.choice(range(3))
        newids = random.choice(hashids)
        dic = {'tag': tag, 'userid': userid, 'alertids': newids}

    elif tag == 'seen': 
        userid = random.choice(range(4))
        db = Join.objects.all() 
        hashids = [n.hashid for n in db]
        nitems = random.choice(range(1,3))
        newids = list(random.sample(hashids, nitems))
        dic = {'tag': tag, 'userid': userid, 'seenids': newids}

    elif tag == 'save': 
        userid = random.choice(range(4))
        db = Join.objects.all() 
        hashids = [n.hashid for n in db]
        nitems = random.choice(range(1,3))
        newids = list(random.sample(hashids, nitems))
        dic = {'tag': tag, 'userid': userid, 'saveids': newids}

    elif tag == 'listing': 
        dic = {"tag": 'listing', "id":379,"slug":"299-graham-avenue-2","title":"Williamsburg, 3 bedrooms","bedrooms":3,"bathrooms":1,"neighborhood":"Williamsburg","parent_neighborhood":\
        {"id":11,"name":"Brooklyn","parent_neighborhood":'null'},"price":1200,"image_url":"/attachments/store/fit/250/120/d679df1b5cf978ebd6e5ef204fbcdd1ce90da7e0c752697c3b8af333fce1/image",\
        "price_string":"$1,200","available_date":"2016-08-01","full_address":"299 Graham Avenue, 11211","listing_type_text":"Share","created_at":"2016-03-30T00:09:29.000-04:00","views":373,\
        "messages":49,"images":11}

    print "The dictionary is :", getframeinfo(currentframe()).lineno, dic
    # data = urllib.urlencode(dic)
    data=json.dumps(dic)
    # data = json.dumps(dic)
    headers = {'content-type': 'application/json'}
    # print "This is the dictionary at: ", getframeinfo(currentframe()).lineno, data
    # req = urllib2.Request(url, data, {})
    print "the url is:", url
    r=requests.post(url, data=data, headers=headers)
    # print r 
    # req = urllib2.Request(url)
    # req.add_header('Content-Type', 'application/json')
    # urllib2.urlopen(req)



def calsearchhashid(search): 
    sn = search["neighborhood"]
    # print sn
    nh, parentarea, area = matchallneighbor(sn)
    # print "This is the hashcode: ", nh
    minprice = '00'
    maxprice = '00'
    beds = '0'
    baths = '0'
    apt = '1'

    if "minprice" in search: 
        minprice = str(int(min(search["minprice"]/100, 99))).zfill(2)[:2]
    if "maxprice" in search: 
        maxprice = str(int(min(search["maxprice"]/100, 99))).zfill(2)[:2]

    if "bedroom" in search: 
        tempbed = str(search["bedroom"])
        if tempbed.isdigit():
            beds = str(int(min(beds, 7)))
        else: 
            if tempbed =='studio':
                beds = '8'
            elif tempbed == 'loft':
                beds = '9'
    if "listing_type_text" in search: 
        tempapt = serach["listing_type_text"]
        if tempapt == 'room': 
            apt = '0'

    return int(str(nh)+minprice+maxprice+beds+baths+apt)


def updatehashid(): 
    temp = Join.objects.all() 

    for e in temp: 
        tempbedroom = e.bedrooms 
        tempbathroom = e.bathroom 
        tempprice = e.price
        tempaddress = e.address
        tempneighborhood = e.neighborhood

    # print sn
        tempneighbhashid, parent, area = matchallneighbor(tempneighborhood)
        # print "This is the hashcode: ", nh
        price = '0000'
        beds = '0'
        baths = '0'
        apt = '1'

        if tempprice:
            price = str(int(tempprice/10)).zfill(4)[:4]

        if "bedroom" in search: 
            tempbed = str(search["bedroom"])
            if tempbed.isdigit():
                beds = str(int(min(beds, 7)))
            else: 
                if tempbed =='studio':
                    beds = '8'
                elif tempbed == 'loft':
                    beds = '9'
        if "listing_type_text" in search: 
            tempapt = serach["listing_type_text"]
            if tempapt == 'room': 
                apt = '0'

        HID = int(str(tempneighbhashid)+minprice+maxprice+beds+baths+apt)
        oldhash = e.hashid
        e.hashid = HID
        e.save 
    

# # bedroom is a string, 2 for hash, 1 for bd/ba, 1 for type, 2 for minprice,2 for maxprice
# def searchHash(dic):
#     bedsdict = {'studio': '8', 'loft': '9'}
#     listdict = {'apartment' : '1', 'room' : '2', 'studio' : '1', 'loft' : '1'}
    
#     neighborhood = dic.get('neighborhood')
#     list_type = dic.get('listing_type_text')
#     bedroom = dic.get('bedroom')
#     bathroom = dic.get('bathroom')
#     minprice = dic.get('minprice')
#     maxprice = dic.get('maxprice')
#     neighborhid = '00000000' 
#     #Hash for neighborhood
#     if neighborhood:
#         nid = getNeighborHash(neighborhood).zfill(8)[:8]
        
#     hid = nid
    
  
#     #Hash for listing
#     hid += listdict[list_type.lower()]
#     #Hash for beds 
#     if bedroom:
#         beds = str(bedroom)
#         if beds.isdigit():
#             hid += beds.zfill(1)[:1]
#         else: 
#             hid += bedsdict[beds]
#     else:
#         hid += '0'
    
#     #Hash for bathroom
#     if bathroom:
#         hid += str(int(math.floor(bathroom)))
#     else: 
#         hid += '0'
#     #Hash for price
#     minid = '00'
#     if minprice: 
#         minid = str(int(min(minprice/100, 99))).zfill(2)[:2]
#     hid += minid
    
#     maxid='99'
#     if maxprice and maxprice < 10000:
#         maxid = str(int(min(maxprice/100, 99))).zfill(2)[:2]
#     hid += maxid
        
#     # print('Hash ID For Neighborhood: ')
#     # print(hid[:8])
    
#     # print('\nHash ID For Search:')
#     # print(hid)
#     return int(hid)

def converttime2utc(time): 
    return time

def saveuserdata(data):
    tag = data['tag']
    # print "line:", getframeinfo(currentframe()).lineno, " And the tag is :", data
    if tag == 'search': 
        a = Userhist.objects.filter(userid =data['userid'])
        # print "the lan of a is: ", len(a)
        searchlist = []
        if len(a)>0:
            tempa = a[0]
            currentsearch = tempa.searchhist
            if currentsearch: 
                searchlist = json.loads(currentsearch)
            else:
                searchlist = []

            # print "the current search list:", searchlist
            searchhashid = calsearchhashid(data)
            # print getframeinfo(currentframe()).lineno, searchhashid
            searchlist.append(searchhashid)
            newhist  = json.dumps(searchlist)
            # print "new search history is: ", newhist
            while len(newhist)>=1000:
                # print "removing item"
                searchlist.pop(0)
                newhist  = json.dumps(searchlist)

            tempa.searchhist = newhist
            tempa.save()

        else: 
            # print getframeinfo(currentframe()).lineno
            searchhashid = calsearchhashid(data)
            searchlist.append(searchhashid)
            udic = {'userid': data['userid'], 'searchhist': json.dumps(searchlist)}
            # print getframeinfo(currentframe()).lineno, udic
            tempa = Userhist(**udic)
            try:
                # print getframeinfo(currentframe()).lineno
                tempa.save()
                # return (hashidlist, N)
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))


    elif tag == "alert": 
        a = Userhist.objects.filter(userid =data['userid'])
        # print "The length of a is: ", len(a)
        searchlist = []
        if isinstance(data["alertids"], int):
            newlist = [data["alertids"]]
        else: 
            newlist = data["alertids"]

        if len(a)>0: 
            tempa = a[0]
            currrentalert = tempa.alerthist
            # print getframeinfo(currentframe()).lineno, currrentalert
            if currrentalert: 
                alertdict = json.loads(currrentalert)
                for n in newlist:
                    if n not in alertdict["alertids"]:
                        alertdict["alertids"].append(n)
            else: 
                alertdict = {'requestid': int(0), 'alertids':newlist}


            newalertlist = json.dumps(alertdict)
            # print "the new data after alert is :", newdata
            while len(newalertlist)>=1000:
                alertdict["alertids"].pop(0)
                newalertlist = json.dumps(alertdict)

            tempa.alerthist = newalertlist
            # print getframeinfo(currentframe()).lineno, tempa.userid, tempa.searchhist, tempa.alerthist, tempa.seenhist
            tempa.save()

        else:
            alertdict = {'requestid': [], 'alertids': newlist}
            newalertlist = json.dumps(alertdict)
            udic = {'userid': data['userid'], 'alerthist': newalertlist}
            tempa = Userhist(**udic)
            try:
                # print getframeinfo(currentframe()).lineno
                tempa.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

    
    elif tag == "alertrequest": 
        a = Userhist.objects.filter(userid =data['userid'])
        # print len(a)
        requestid = calsearchhashid(data)
        if len(a)>0: 
            tempa = a[0]
            currrentalert = tempa.alerthist
            # print "alert hist :", currrentalert
            if currrentalert: 
                alertdict = json.loads(currrentalert)
                if isinstance(alertdict["requestid"], int):
                    alertdict["requestid"] = [alertdict["requestid"]]
                alertdict["requestid"].append(requestid)
            else: 
                alertdict = {'requestid': [requestid], 'alertids': []}
            # print "the hashid of the request:", requestid
            newalerthist  = json.dumps(alertdict)
            while len(newalerthist)>=1000:
                alertdict["requestid"].pop(0)
                newalerthist = json.dumps(alertdict)
            # print "new user data after alert request: ", newdata
            tempa.alerthist = newalerthist
            tempa.save()

        else: 
            requestid = calsearchhashid(data)
            alertdict = {'requestid': [requestid], 'alertids': []}
            newalerthist = json.dumps(alertdict)
            udic = {'userid': data['userid'], 'alerthist': newalerthist}
            # print "the new dictionary for alert request:" , udic
            tempa = Userhist(**udic)
            try:
                # print getframeinfo(currentframe()).lineno
                tempa.save()
                # return (hashidlist, N)
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))


    elif tag == "seen": 
        a = Userhist.objects.filter(userid =data['userid'])
        # print getframeinfo(currentframe()).lineno, len(a)
        if "seenids" not in data: 
            return 

        if isinstance(data["seenids"], int):
            newlist = [data["seenids"]]
        else: 
            newlist = data["seenids"]

        if len(a)>0: 
            tempa = a[0]
            currentseen = tempa.seenhist
            if currentseen:
                seenlist = json.loads(currentseen)
                for s in newlist: 
                    if s not in seenlist: 
                        seenlist.append(s)
            else: 
                seenlist = newlist

            newhist  = json.dumps(seenlist)
            # print "new json hist is:", newhist
            while len(newhist)>=1000:
                seenlist.pop(0)
                newhist  = json.dumps(seenlist)

            tempa.seenhist = newhist
            tempa.save()

        else:
            newhist = json.dumps(newlist)
            udic = {'userid': data['userid'], 'seenhist': newhist}
            tempa = Userhist(**udic)
            try:
                tempa.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

    elif tag == "save": 
        a = Userhist.objects.filter(userid =data['userid'])
        # print getframeinfo(currentframe()).lineno, len(a)
        if "saveids" not in data: 
            return 

        print "Now we are in the save part: ", data
        if isinstance(data["saveids"], int):
            newlist = [data["saveids"]]
        else: 
            newlist = data["saveids"]

        print "This is the new ID list :", newlist
        if len(a)>0: 
            tempa = a[0]
            currsave = tempa.savehist
            if currsave:
                print "The current save list exist"
                slist = json.loads(currsave)
                for s in newlist: 
                    if s not in slist: 
                        slist.append(s)
            else: 
                slist = newlist

            print "So, the save list is:", slist
            newhist  = json.dumps(slist)
            # print "new json hist is:", newhist
            while len(newhist)>=1000:
                slist.pop(0)
                newhist  = json.dumps(slist)

            tempa.savehist = newhist
            tempa.save()

        else:
            newhist = json.dumps(newlist)
            udic = {'userid': data['userid'], 'savehist': newhist}
            tempa = Userhist(**udic)
            try:
                tempa.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

    elif tag == 'listing': 
        listing_dict = {}
        attributes = ['neighborhood', 'full_address', 'bedrooms', 'bathrooms', 'price', 'listing_type_text', 'title', 'price', 'parent_neighborhood', 'image_url', 'available_date', 'created_at', 'views', 'messages', 'slug', 'images'] 
        dic = {'slug': 'url'}
        
        for a in attributes: 
            if a in data: 
                # print a, type(data[a]) , data[a]
                if a == 'parent_neighborhood': 
                    listing_dict[a] = json.dumps(data[a])
                if data[a] == 'null': 
                    data.pop(a) 
                if a in dic:
                    if a == 'slug':
                        listing_dict[dic[a]] = "https://joinery.nyc/listing/" + data[a]
                    else: 
                        listing_dict[dic[a]] = data[a]
                else: 
                    if a == 'image_url': 
                        listing_dict[a] = "https://joinery.nyc/" + data[a]
                    elif a == 'created_at': 
                        listing_dict[a] = converttime2utc(data[a])
                    else:
                        listing_dict[a] = data[a]


        listing_dict['source'] = 'joinery'
        SID = calhashid(listing_dict['bedrooms'], listing_dict['neighborhood'], listing_dict['full_address'], listing_dict['price'], listing_dict['source'], listing_dict['listing_type_text'])
        listing_dict['hashid'] = SID
        # print "The dict before saving in db:", listing_dict
        insert2db([listing_dict])
        return SID

    elif tag == 'match_address': 
        h, p, n = matchallneighbor(data['neighborhood'])
        url = "https://mighty-shelf-86819.herokuapp.com/"
        dic = {'neighborhood': n, 'parent_neighborhood': p}
        import requests
        data=json.dumps(dic)
        # data = json.dumps(dic)
        headers = {'content-type': 'application/json'}
        # print "This is the dictionary at: ", getframeinfo(currentframe()).lineno, data
        # req = urllib2.Request(url, data, {})
        r=requests.post(url, data=data, headers=headers)




#Rounds up math function
def roundUp(x, dig):
    import math
    return int(math.ceil((x + .5) / float(dig))) * dig

#returns a list of the areas with the same first Letter
def fillList(c, list):
    results = []
    for n in list:
        if c == n.area[0]:
            results.append(n.area)
    return results

from pprint import pprint

#62 Unique parent Neighborhoods
def updateShortNHash():
    neighborhoods = Neighborhood.objects.order_by('parentarea','area')
    parentN = []#List of unique parent Neighborhoods 62 / 37 truly unique 
    N = []#List of unique neighborhoods 455 / 673 unique neighborhoods with dif pA
    parentInfo = [] # List of dicts to contain all information 
    areas = {}#Dict of areas and short hash

    #Hashi is '0000'
    sIDict = {'Manhattan': 10 ,'Brooklyn': 25 ,'Bronx': 40 ,'Queen': 55, 'Staten' : 70, 'Jersey' : 78 } #parent hash for boroughs
    aIDict = {'Manhattan': 0 ,'Brooklyn': 0 ,'Bronx': 0 ,'Queen': 0, 'Staten' : 0, 'Jersey' : 0} #area hash for boroughs

    prevPa = ''
    preva = ''
    prevInd = ''
    prevMat = ''

    otherIndex = 0

    # Fixes parentAreas
    for n in neighborhoods:
        if n.parentarea:
            n.parentarea = n.parentarea.strip()
            n.save()
    
    count = 0
    for n in neighborhoods:
        pArea=n.parentarea
        a =  n.area

        if pArea  not in parentN:
            parentN.append(pArea)

        if a not in N:
            N.append(a)

        #Finds a match for a borough in parentArea
        match = next((s for s in sIDict if s in pArea),False)

      
        #Filters the Neighborhood object
        filArea = Neighborhood.objects.filter(parentarea = pArea)

        #Holds the list of Dic for areas
        div = []

        #Index relative to the number of childs 
        index = 0
        #if match:
         #   index = aIDict[match];

        #Determines how many repeats there are
        repeat = 0

        #fills the list of Dic and finds the index
        for i in filArea:
            #print i.area , i.parentarea
            if not any(i.area[0] in d for d in div):
                
                div.append({i.area[0] : fillList(i.area[0], filArea)})
                
                if a[0] > i.area[0]:
                    index += 1
            if a == i.area: 
                repeat+=1
            
        dif = 0
        
        if pArea:
            dif = ord(a[0]) - ord('A')

        #If parent is in borough
        if match:
            shid = str(sIDict[match]).zfill(2)[:2]
          #If the pArea is not part of the boroughs, then the first hash becomes 0 or 8-9
        else:
          
            if pArea:
                
                #Checks if this is a new area in the parentArea
                if preva != a and prevPa == pArea and a[0] != prevInd:
                    otherIndex = roundUp(otherIndex,10) 
                #Increments if not repeat
                elif repeat < 2 or preva != a:
                    otherIndex+=4
                
                #Checks if this is a new parentArea
                if prevPa != pArea:
                    otherIndex = roundUp(otherIndex, 20)
                    
                #Assigns shid
                shid = '8' + str(otherIndex%1000).zfill(3)[:3]
                if otherIndex > 999:
                    shid = '9' + str(otherIndex%1000).zfill(3)[:3]
                
                
                if otherIndex > 2000:
                    print 'Error: Too many other neighborhoods, decrease incrementation'
                    raw_input()
                    print otherIndex
                    break
            
                
            #If there is no parent Area, then the first hash becomes 0
            else:
                tmp = ord(a[0]) % 10
                tmpmatch = next((s for s in sIDict if s in a),False)
                
                if tmpmatch:
                    tmp = sIDict[tmpmatch]
                
                shid = '0' + str(tmp).zfill(1)[:1]
            

        if shid[0] not in ['8', '9'] :
           
                
            if match:

                spacingB = {'Manhattan': 6 ,'Brooklyn': 8 ,'Bronx': 12 ,'Queen': 12, 'Jersey' : 6, 'Staten': 6} #index for borough

                if preva != a and prevPa == pArea and a[0] != prevInd:
                     aIDict[match] = roundUp( aIDict[match], 10) 
                elif repeat < 2 or preva != a:
                    aIDict[match] += spacingB[match]
                
                if prevPa != pArea and match == prevMat or prevMat != match:
                    aIDict[match] += roundUp(aIDict[match], 100)
                

                    
                if aIDict[match] > 99:
                    sIDict[match] += 1
                    aIDict[match] = 0
                    shid = str(sIDict[match]).zfill(2)[:2]

                aid = str(aIDict[match]).zfill(2)[:2]
            else:
                aid = str(index%10) + '0'
                      
            shid += aid
            currentindex = index

        if match == 'Bronx':
            pass
            #print 'parent Area: ' + pArea, 'Area: ' + a,'Shid ' + shid
        
        preva = a
        prevInd = a[0]
        prevPa = pArea
        prevMat = match

        #For debugging
        parentInfo.append({'parentarea': pArea, 'area' : a, 'shid' : shid})
        if a in areas:
            print 'You need to change parentArea of ',a
        areas[a] = shid
        n.shid = int(shid) 
        n.save()


def calneighborshorthash():
    prevarea = None
    newshid = 0
    bDict = {'Manhattan': 1000 ,'Brooklyn': 2500 ,'Bronx': 4000 ,'Queen': 5500, 'Staten' : 7000, 'Jersey' : 7800 } #parent hash for boroughs

    neighborhoods = Neighborhood.objects.order_by('parentarea','area','shid')
    sortedList = Neighborhood.objects.order_by('shid')

    c = 0
            
    for n in neighborhoods:
        
        pa = n.parentarea
        a = n.area
        shid = n.shid
        
        if shid == 0 or shid>9999:
            duparea = Neighborhood.objects.filter(parentarea = n.parentarea, area=n.area)
            if len(duparea) > 1:
                for d in duparea: #Finds if the area is a dup of another
                    if d.shid != 0:
                        # print 'It is a dup'
                        shid = d.shid
                        # print d.shid
                        break

            if shid == 0:
                match = next((s for s in bDict if s in pa),False)
                print 'Not a dup'
                
                #print prevarea.parentarea,prevarea.area,prevarea.shid
                #Bounds to search
                upperbound = 10000
                lowerbound = 0
                if prevarea:
                    lowerbound = prevarea.shid
                
                if match:
                    lowerbound = bDict[match]
                    upperbound = bDict[match] + 1500
                    #Sets the prev area again
                    prevarea = None
                    prevlist = sortedList.filter(parentarea__lte=pa,area__lt=a, shid__gt=lowerbound, shid__lt=upperbound).reverse()
                    if not prevlist:
                        prevlist = sortedList.filter(parentarea__lt=pa, shid__gt=lowerbound, shid__lt=upperbound).reverse()
                    if prevlist:
                       prevarea = prevlist[0]

                nextarea = None
                nextlist = sortedList.filter(parentarea__gte=pa,area__gt=a, shid__gt=lowerbound, shid__lt=upperbound)
                if nextlist:
                    nextarea = nextlist[0]

                    
                #print prevarea.parentarea,prevarea.area,prevarea.shid
                #print nextarea.parentarea,nextarea.area,nextarea.shid
                
                if nextarea and prevarea: #General case
                    dif = nextarea.shid - prevarea.shid
                    newshid = prevarea.shid + dif/2
                        
                    # print int(newshid)
                elif nextarea: #For first item case
                    dif = nextarea.shid - lowerbound
                    newshid = lowerbound + dif/2
                        
                    # print int(newshid)
                else: #For last item case
                    dif = upperbound - prevarea.shid
                    newshid = prevarea.shid + dif/2
                    # print int(newshid)
     
            if newshid == 0:
                print 'Error'
                 
            if n.shid != int(newshid):
                n.shid = int(newshid)
                n.save()

        prevarea = n



def distance(origin, destination):
    import math
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def updateparentneighborhood(): 
    tempneighborhood = Join.objects.all() 
    for n in tempneighborhood: 
        source = n.source
        m = match_address(source, n.neighborhood)
        if m[0]>0: 
            n.neighborhood = m[1]
            n.parent_neighborhood = m[0]
            n.save()

def findparentlisting(area, queryset): 
    parentdict = makeListofSamePArea()
    # print "Start the find parent lisitng (area):", area
    condition = Q(neighborhood = area)

    nb = Join.objects.filter(condition)

    parentset = set([e.parent_neighborhood for e in nb if e.parent_neighborhood != area])
    tempset = set([])
    for p in parentset: 
        if p in parentdict: 
            tempset.update(parentdict[p])

    parentset.update(tempset)
    parentlist = list(parentset)
    # print "The parents are: ", parentlist
    newlistings = []
    # searchdic = {'pricemin': pricemin, 'pricemax':pricemax, 'beds':beds, 'baths':baths}
    # attdic = {'pricemin': 'price__gte', 'pricemax':'price__lte', 'beds': 'bedroom', 'baths':'bathroom'}
    # cleaneddict = {k: dic[k] for k in searchdic if searchdic[k]}

    # for k in cleaneddict: 
        # queryset = queryset.filter(attdic[k] = searchdic[k])
    condition = Q()
    for p in parentlist: 
        condition = condition | Q(parent_neighborhood = p) | Q(neighborhood = p)

    # print "The conditions are: ", condition

    newqueryset = queryset.filter(condition) 
    # newlistings += [e for e in newqueryset]

    # print "New parent listings are:", len(newqueryset)

    # if len(querylist)<10: 
    #     if parent: 
    #         parentdict = {""}
    #         print "The number of items in the area is very low, we follow the parent area:"
    #         print parent
    #         templs = [e for e in Join.objects.filter(parent_neighborhood = parent, price__lte = pricemax, price__gte = pricemin)]
    #         print "The parent results are :", len(templs)
    #         print type(templs), type(ls)
    #         querylist += templs 
    #         print "The new list is: ", len(templs)

    #     else: 
    #         print "The number of items are low and we try with different bedroom and bathroom number"
    #         templs = [e for e in Join.objects.filter(price__gte = pricemin, price__lte = pricemax)] 
    #         querylist += templs

    # if len(querylist)<10: 
    #     pass

        # distancedic = {}
        # for n in nb: 
        #     latemp = n.latitude
        #     lngemp = n.longitude
        #     hashid = n.hashid 
        #     d = distance((lat, lng), (latemp, lngemp))
        #     distancedic[hashid] = d 
        #     # print (lat, lng), (latemp, lngemp), d 

        # sortedhashids = sorted(distancedic.items(), key=lambda x: x[1])

        # for i in range(10): 
        #     item = sortedhashids[i]
        #     print item 
        #     if item[1]>1: 
        #         break 
        #     hashid = item[0]
        #     tempobj = Neighborhood.objects.filter(hashid = hashid)[0]
        #     print tempobj.area
        #     newlist = Join.objects.filter(neighborhood = tempobj.area, price__gte = pricemin, price__lte = pricemax) 
        #     print len(newlist)
        #     if beds: 
        #         newlist = newlist.filter(bedroom = beds)
        #     if baths: 
        #         newlist = newlist.filter(bathroom = baths)

        #     print len(newlist)
        #     ls +=newlist

    # print "The new number of results: ", len(ls)
    # for e in querylist: 
    #     print e.neighborhood, e.parent_neighborhood, e.price, e.hashid 

    # print [e.hashid for e in querylist]

    return (newqueryset, parentlist)



def makeListofSamePArea():
    from django.db import connection
   
    ppArea_Query = 'select area, pparea, count(distinct parentarea) from joins_neighborhood as A  natural join (select area as parentarea, parentarea as pparea from joins_neighborhood) as B group by area, pparea order by area, pparea ;'

    c = connection.cursor()
    boroughs = ['Manhattan', 'Queens', 'Brooklyn', 'Staten Island', 'New Jersey', 'Bronx', 'NYC']
    
    c.execute(ppArea_Query)

    data = c.fetchall()

    samePArea = {}
    
    for d in data:
      
        if(int(d[2]) > 1):
            c.execute("select distinct parentarea from joins_neighborhood where area = '%s'" % (d[0])) #Getting parentarea from db
            info = c.fetchall() 
        
            templ = []
            for i in info:
                if not any(s == i[0] for s in boroughs):
                    templ.append(i[0])

            if len(templ) > 1:
                for p in templ:
                    if p in samePArea:
                        samePArea[p] += [i for i in templ if i != p and i not in samePArea[p]]
                    else: samePArea[p] = [i for i in templ if i != p]
    
    return samePArea

def calnumbersimilarity(h1, h2): 
    sh1 = str(h1)
    sh2 = str(h2)
    dif = 0.

    first = Join.objects.get(hashid = h1)
    second = Join.objects.get(hashid = h2)

    p1 = first.price
    p2 = second.price
    a1 = first.full_address
    a2 = second.full_address
    b1 = first.bedrooms 
    b2 = second.bedrooms 

    if p1 == p2 and a1 == a2 and b1 == b2:
        return 1

    for i,j in zip(sh1,sh2):
        if i != j: dif+=1./len(sh1)

    # print 'Sim: %i percent' %(dif)
    return dif


def reverseHash(hid):
    bedsdict = {'8' : 'studio', '9' : 'loft' }
    listdict = {'1' : 'apartment', '2' : 'room',  '3' : 'studio', '4' : 'loft'}

    hid = str(hid)
    print('\nInfo For Neighborhood: ')
    nid = hid[:8]
    getNeighborHood(nid)

    hid = hid[8:]

    print("\nListing type is : " + listdict[hid[0]])
    
    if hid[1] < '8':
        print("Searching for " + hid[1] + " bedrooms")
    else:
        print("Searching for " + bedsdict[hid[1]] + " bedrooms")

    print("Searching for " + hid[2] + " bathrooms ")

    print("Searching for " + hid[3:5] + "00 min price")

    print("Searching for " + hid[5:7] + "00 max price")



def getTimeDifference(date):
    dif = str(datetime.datetime.now().replace(tzinfo=None) - date.replace(tzinfo=None)).rpartition('days')[0]    
    
    tdif = 0
    if dif:
        tdif = int(dif)
    return tdif

def makeRankedList(hashlist,neighborhood, weights= {'time' : 1., 'price' : 0., 'distance': 1.}):
    
    timeW = weights['time']
    priceW = weights['price']
    distW = weights['distance']


    rankscore = {}

    neighbhashid, parent, neighborhood = matchallneighbor(neighborhood)
    obj = Neighborhood.objects.filter(hashid = neighbhashid)[0]
    lat = obj.latitude
    lng = obj.longitude


    distancedic = {}
    pricedic = {}
    timedic = {}



    for h in hashlist:

        j = Join.objects.filter(hashid = h)[0]
        jneigh = j.neighborhood


        lat2, lng2 = scodes.updatelatlng(j)
        if lat and lng: 
            d = distance((lat,lng),(lat2,lng2))
            distancedic[h] = d

        else: 
            distancedic[h] = 5

        if 'T' in j.created_at: 
            j.created_at = j.created_at.replace('T', ' ')[:15]
            j.save()

        created_at = datetime.datetime.strptime(j.created_at[:15], '%Y-%m-%d %H:%M')

        tdif = getTimeDifference(created_at)

        price = j.price #- pricemin ?

        timedic[h] = tdif

    sorteddistance = sorted(distancedic.items(), key=lambda x: x[1])
    sortedprice = sorted(pricedic.items(), key=lambda x: x[1])
    sortedtime = sorted(timedic.items(), key=lambda x: x[1])

    
    # #Get the neigborhood information
    

    N = 30
    # #====================Gets the distance from a local address
    # distancedic = distancedic.copy()
    # for item in sorteddistance[:min(N, len(sorteddistance))]: 
    #     s = item[0]
    #     l = Join.objects.filter(hashid = s)
    #     if l : 
    #         l = l[0]
    #     else: 
    #         distancedic[s] = distancedic[s]
    #         continue
    #     # l = ls.get(hashid = s[0])
    #     # print l.hashid, l.neighborhood, l.full_address
    #     address = l.full_address if l else None 
    #     parent_neighborhood = l.parent_neighborhood if l else None 
    #     neighborhood = l.neighborhood if l else None 
    #     dic = {}
    #     if not address:
    #         distancedic[s] = distancedic[s]
    #         continue
    #     else: 
    #         templist = [address, neighborhood, parent_neighborhood]
    #         templist = [e for e in templist if e]
    #         tempaddress = ' '.join(templist)
    #         dic = {"address": tempaddress}

    #     url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(dic)
    #     try:
    #         response = urllib2.urlopen(url)
    #         data = json.load(response) 
    #         if "results" in data:
    #             latemp = data["results"][0]["geometry"]['location']['lat']
    #             lngemp = data["results"][0]["geometry"]['location']['lng']
    #             d = distance((lat, lng), (latemp, lngemp))
    #             distancedic[s] = d if d < max(2,3*distancedic[s]) else distancedic[s]
    #         else : 
    #             distancedic[s] = distancedic[s]
    #             continue
    #     except: 
    #         distancedic[s] = distancedic[s]
    #         print "Connection problem"
    #         continue
            
    #=====================================================================
    meandistance = sum(distancedic.values())/len(distancedic.values())
    meanprice = sum([s[1] for s in sortedprice][:min(N, len(sortedprice))])/float(min(N, len(sortedprice)))
    meantime = sum([t[1] for t in sortedtime][:min(N,len(sortedtime))])/float(min(N,len(sortedtime)))

    rankscore = {}


    print meandistance, meanprice, meantime
    for i in range(min(N, len(sorteddistance))): 
        s = sorteddistance[i][0]
        print pricedic[s],
        pricedic[s] = pricedic[s]*((meandistance+1.)*(meantime+1.))/(meanprice+1.)
        print s, distancedic[s], pricedic[s], timedic[s]
        print distancedic[s] if s in distancedic else None
        rankscore[s] = weights['time'] * timedic[s] + weights['price'] * pricedic[s] + 0 + weights['distance'] * distancedic[s] #+ distancedic[s]
        #rankscore[s] = pricedic[s] + distancedic[s]

        
    #rankscore[i] = weights['time'] * timedict[i] + distancedic[i]a
    
    sortedscore = sorted(rankscore.items(), key=lambda x: x[1])
    removeindex = set([])
    for i in range(len(sortedscore)): 
        for j in range(i): 
            simil = calnumbersimilarity(sortedscore[i][0], sortedscore[j][0])
            if simil>0.7:
                removeindex.add(j)

    print removeindex
    sortedscore = [v for i, v in enumerate(sortedscore) if i not in removeindex]
    finallist = [s[0] for s in sortedscore][:min(N, len(sortedscore))]
    

    for f in finallist:
        j = Join.objects.filter(hashid = f)
        print 'Looking in neighborhood: ', neighborhood
        print 'Todays Date is ',datetime.datetime.now()
        j = j[0]
        print 'Days:', timedic[f], ' Price:', pricedic[f], 'Distance:', distancedic[f]
        print j.price, j.neighborhood, j.created_at, j.source
        print ''


    return finallist


def findranklisting(data):
    # print parentdict
    # print "The received data is:", data
    neighborhood = data["neighborhood"]
    pricemin = data['minprice']
    pricemax = data['maxprice']
    beds = data['bedroom'] if 'bedroom' in data else None
    baths = data['bathroom'] if 'bathroom' in data else None
    dicW = {'time' : 1., 'price' : 1., 'distance': 1.}


    # print "it is ok"
    # dic = {"neighborhood": "Queens", "userid": 3, "maxprice": 2808, "tag": "search", "bedroom": "loft", "minprice": 1775}
    neighbhashid, parent, neighborhood = matchallneighbor(neighborhood)

    # print "The matched data area:", neighbhashid, parent, neighborhood
    obj = Neighborhood.objects.filter(hashid = neighbhashid)
    if obj:
        obj = obj[0]
    else:
        print 'Nohing Found'
        return None
    lat = obj.latitude
    lng = obj.longitude
    ls = Join.objects.filter(price__lte = pricemax, price__gte = pricemin)
    # print " The length after price: ", len(ls)

    condition = Q(bedrooms = beds) 
    if beds:
        if beds == 'loft':
            ls = ls.filter(bedrooms = beds)
        elif beds!='studio': 
            ls = ls.filter(bedrooms__gte = beds).exclude(bedrooms = 'studio').exclude(bedrooms = 'loft')
    # if baths: 
    #     ls = ls.filter(bathrooms = baths)

    print "The number of results after bedroom and bathrom : ", len(ls) 

    # queryset = ls.clone() 
    # print "clone is done"
    condition = Q(neighborhood = neighborhood) | Q(parent_neighborhood = neighborhood)

    newqueryset = ls.filter(condition)
    queryset = set([e for e in newqueryset])
    
    #rankscore =  makeRankedList(hashlist, neighborhood, dicW, dicMean)   
    # print "the number of results after neighborhood :", len(newqueryset)
    
    nset = set([neighborhood])
    N = 10
    while len(queryset)<N:
        # print "The query set size is : ", len(queryset)
        # print "Then neighborhood list is :", len(nset)  
        parentset = set([])

        for n in nset:
            if n: 
                newqueryset, temp = findparentlisting(n, ls)
                parentset.update(temp)
                # print "parent neighborhood and the reslut length: ", n, len(newqueryset)
                queryset.update([e for e in newqueryset])
                # print len(queryset), " listings including the ones in ", n

        nset = parentset
        # print "The new neighborhood set is: ", len(nset), nset
        # nlist = list(set([e.parentarea for e in Neighborhood.objects.filter(area = neighborhood)]))
        if not nset: 
            break

    print "The FINAL number of results: ", len(queryset)


    hashlist = [q.hashid for q in queryset]

    print hashlist
    #raw_input()
    weights= {'time' : 1., 'price' : 0., 'distance': 1.}

    return makeRankedList(hashlist, neighborhood, weights)


def findlisting(data, foundhashlist = []):
    # print parentdict
    # print "The received data is:", datadef makeRankedList(hashlist,neighborhood, weights= {'time' : 1., 'price' : 1., 'distance': 1.})
    finallist = foundhashlist
    removeindex = set([])
    for i in range(len(finallist)): 
        for j in range(i): 
            simil = calnumbersimilarity(finallist[i], finallist[j])
            if simil>0.75:
                removeindex.add(j)

    print removeindex
    finallist = [v for i, v in enumerate(finallist) if i not in removeindex]

    finallist = finallist[:min(10, len(finallist))]



    # if len(finallist)<5:
    #     neighborhood = data["neighborhood"]
    #     pricemin = data['minprice']
    #     pricemax = data['maxprice']
    #     beds = data['bedroom'] if 'bedroom' in data else None
    #     baths = data['bathroom'] if 'bathroom' in data else None
    #     # print "it is ok"
    #     # dic = {"neighborhood": "Queens", "userid": 3, "maxprice": 2808, "tag": "search", "bedroom": "loft", "minprice": 1775}
    #     neighbhashid, parent, neighborhood = matchallneighbor(neighborhood)
    #     # print "The matched data area:", neighbhashid, parent, neighborhood
    #     obj = Neighborhood.objects.filter(hashid = neighbhashid)[0]
    #     lat = obj.latitude
    #     lng = obj.longitude
    #     ls = Join.objects.filter(price__lte = pricemax, price__gte = pricemin)
    #     # print " The length after price: ", len(ls)

    #     condition = Q(bedrooms = beds) 
    #     if beds:
    #         if beds == 'loft':
    #             ls = ls.filter(bedrooms = beds)
    #         elif beds!='studio': 
    #             ls = ls.filter(bedrooms__gte = beds).exclude(bedrooms = 'studio').exclude(bedrooms = 'loft')
    #     # if baths: 
    #     #     ls = ls.filter(bathrooms = baths)

    #     print "The number of results after bedroom and bathrom : ", len(ls) 

    #     # queryset = ls.clone() 
    #     # print "clone is done"
    #     condition = Q(neighborhood = neighborhood) | Q(parent_neighborhood = neighborhood)

    #     newqueryset = ls.filter(condition)
    #     # print "the number of results after neighborhood :", len(newqueryset)
    #     queryset = set([e for e in newqueryset])
    #     nset = set([neighborhood])
    #     N = 50
    #     while len(queryset)<N:
    #         # print "The query set size is : ", len(queryset)
    #         # print "Then neighborhood list is :", len(nset)  
    #         parentset = set([])

    #         for n in nset:
    #             if n: 
    #                 newqueryset, temp = findparentlisting(n, ls)
    #                 parentset.update(temp)
    #                 # print "parent neighborhood and the reslut length: ", n, len(newqueryset)
    #                 queryset.update([e for e in newqueryset])
    #                 # print len(queryset), " listings including the ones in ", n

    #         nset = parentset
    #         # print "The new neighborhood set is: ", len(nset), nset
    #         # nlist = list(set([e.parentarea for e in Neighborhood.objects.filter(area = neighborhood)]))
    #         if not nset: 
    #             break

    #     print "The FINAL number of results: ", len(queryset)

    #     distancedic = {}
    #     pricedic = {}

    #     for q in queryset: 
    #         n = Neighborhood.objects.filter(area = q.neighborhood)
    #         if n: 
    #             n = n[0]
    #             latemp = n.latitude
    #             lngemp = n.longitude
    #             d = distance((lat, lng), (latemp, lngemp))
    #             hashid = q.hashid 
    #             distancedic[hashid] = d 
    #             pricedic[hashid] = q.price - pricemin



    #     sorteddistance = sorted(distancedic.items(), key=lambda x: x[1])
    #     sortedprice = sorted(pricedic.items(), key=lambda x: x[1])
        
        

    #     meandistance = sum(addressdistance.values())/len(addressdistance.values())#sum([s[1] for s in sorteddistance][:min(N,len(sorteddistance))])/float(min(N, len(sorteddistance)))
    #     # print sorteddistance[:min(N,len(sorteddistance))], meandistance
    #     meanprice = sum([s[1] for s in sortedprice][:min(N, len(sortedprice))])/float(min(N, len(sortedprice)))

    #     print meandistance, meanprice
    #     # for s2 in sortedprice: 
    #     #     s2[1] = s2[1]*meandistance/meanprice
    #     rankscore = {}
    #     for i in range(min(N, len(sorteddistance))): 
    #         s = sorteddistance[i][0]
    #         print pricedic[s],
    #         pricedic[s] = pricedic[s]*(meandistance+1.)/(meanprice+1.)
    #         print s, distancedic[s], pricedic[s],
    #         print addressdistance[s] if s in addressdistance else None
    #         rankscore[s] = pricedic[s] + addressdistance[s]


    #     sortedscore = sorted(rankscore.items(), key=lambda x: x[1])
    #     removeindex = set([])
    #     for i in range(len(sortedscore)): 
    #         for j in range(i): 
    #             simil = calnumbersimilarity(sortedscore[i][0], sortedscore[j][0])
    #             if simil>0.75:
    #                 removeindex.add(j)

    #     print removeindex
    #     sortedscore = [v for i, v in enumerate(sortedscore) if i not in removeindex]
    #     finallist += [s[0] for s in sortedscore][:min(20, len(sortedscore))]

    return finallist




