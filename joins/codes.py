from .models import Join, Neighborhood

import sys, json, base64, os, urllib2
# from ipywidgets import widgets
from bs4 import BeautifulSoup
import codecs
import urllib

import datetime 
import time 
import numpy as np 
import re
import pandas as pd
# from nltk import word_tokenize
from scipy import stats
# import nltk
import collections 
from math import isnan 

# nltk.data.path.append('./nltk_data/')

reload(sys)  
sys.setdefaultencoding('utf8')

global DIV
DIV = 1000000



def call_agent(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    return urllib2.urlopen(req).read()    





def name_similarity(rname, sname): # real name vs similar name 
    N=len(rname)
    Ns=[]
    shift=[-1,0,1]
    accuracy=[]
#     print rname, sname 
    for i in range(len(shift)):
        sh=shift[i]
        if sh<0:
            sn=sname[:sh]
        elif sh>0:
            sn=sname[sh:]
        else:
            sn=sname

        Ns.append(0.)
        for i in range(min(N, len(sn))): 
            if sn[i] == rname[i]: 
                Ns[-1]+=1

        accuracy.append(Ns[-1]/N)
    
    return max(accuracy)
            
    
def match_address(w, adrs): 
    adrs=adrs.lower()
    p=0.8
    if w==0:
        adrsNames=pd.read_csv("Files/streeteasy_neighborhood.csv", index_col=0)
        neighbNames=list(adrsNames["neighborhood"])

        newNeighbs=[x for x in neighbNames]
        nameDict={}
        for n in newNeighbs:
            nameDict[n]=name_similarity(adrs, n)        

        sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
        if sortedNeighbs: 
#             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
            if nameDict[sortedNeighbs[0]]>p:
                level=list(adrsNames[adrsNames['neighborhood']==sortedNeighbs[0]]["level"])[0]
                return (level, sortedNeighbs[0],-1)
            else: 
                return (-1,-1,-1)
        else: 
            return -1
    elif w==1:
        adrs=adrs.lower()
        adrsNames=pd.read_csv("Files/neighborhood_nybits.csv", index_col=0)
        neighbNames=[s.replace('_', ' ') for s in list(adrsNames["Neighbor_codes"])]
        newNeighbs=neighbNames[::]
        nameDict={}
        for n in newNeighbs:
            nameDict[n]=name_similarity(adrs, n)        

        sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
        if sortedNeighbs: 
#             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
            if nameDict[sortedNeighbs[0]]>p: 
                row=adrsNames[adrsNames['Neighbor_codes']==sortedNeighbs[0].replace(' ', '_')]
                code=list(row["Neighbor_codes"])[0]
                level=list(row["level"])[0]
                return (level, sortedNeighbs[0], code)
            else:
                return (-1,-1,-1)
        else: 
#             print "we didn't find any matching name, try again please"
            return -1

    elif w == 'streeteasy':
        adrs=adrs.lower()
        adrsNames=pd.read_csv("Files/neighborhood_nakedapartments.csv", index_col=0)
        neighbNames=list(adrsNames["Neighbor_names"])
        newNeighbs=neighbNames[::]
        nameDict={}
        for n in newNeighbs:
            nameDict[n]=name_similarity(adrs, n)        

        sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
        if sortedNeighbs: 
#             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
            if nameDict[sortedNeighbs[0]]>p: 
                row=adrsNames[adrsNames['Neighbor_names']==sortedNeighbs[0]]
                code=list(row["Neighbor_codes"])[0]
                level=list(row["level"])[0]
                return (level, sortedNeighbs[0], code)
            else: 
                return(-1,-1,-1)
        

        else: 
#             print "we didn't find any matching name, try again please"
            return -1
    elif w == 'nybits': 
        ny_neighborhood_names = open("Files/ny_neighborhood_names.txt", "r")
        newNeighbs=ny_neighborhood_names.read().split('\n')

        querywords=word_tokenize(adrs)
        revisedwords=[]
        for w in querywords:
            nameDict={}
            for n in newNeighbs:
                nameDict[n]=name_similarity(w, n) 
            sortedNeighbs=sorted(newNeighbs, key=lambda x: nameDict[x], reverse=True) 
            revisedwords.append(sortedNeighbs[0])
        
        return (0, '', ' '.join(revisedwords)) 

                
    else: 
        return -1
        

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
    wordcount=collections.Counter(allwords)
    
    for s in nonasciititles: 
        cl=sum([1 for c in s if c.isupper()])
        sl=len(s)
        titlecapitalized.append(float(cl)/sl)
        # words=word_tokenize(str(s))
        words = str(s).split()
        titlerepetitionfactor.append(sum([wordcount[w] for w in words]))

    maxcount=float(max(titlerepetitionfactor))
    repetitionpercentile=[stats.percentileofscore(titlerepetitionfactor, a, 'strict') for a in titlerepetitionfactor]
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
        sid = str(datetimes[-1])
        sid = sid.replace('-', '')
        sid = sid.replace(':','')
        sid = sid.replace(' ', '')

        if len(sid)<8:
            continue


        if isinstance(neighborhoods[-1],basestring):
            temp=ord(neighborhoods[-1][0])
            sid += str(temp).zfill(3)[:3]
        else:
            sid+='000'

        if isinstance(prices[-1],float) or (prices[-1] is None):
            sid+='00'
        else: 
            sid += str(int(prices[-1]/100.)).zfill(2)[:2]

        sid+='1'

        ID.append(sid)

    isbroker=[brokertobool(b) for b in broker]
    beds = [convertbeds(b) for b in beds]
    ID=[int(i) for i in ID]
    # print ID
    pagedict={"hashid": ID, "title":titles, "created_at": datetimes, "listing_type_text": aptorroom, "bedroom": beds, "price":prices, "neighborhood": neighborhoods, "isbroker":isbroker, "linkurl": hreflinks}
    df=pd.DataFrame(pagedict)
    df = add_broker(df)
    df['section'] = section
    df = df[df['hashid'] >= sectionlastdate*DIV]
    if df.shape[0]==0:
        return df

    dfdict = df.to_dict(orient='records')
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

    return df

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
        while j<300:
            sleeptime=10+10*np.random.random()
            # print "I am sleeping for %f seconds"%sleeptime
            time.sleep(sleeptime)
            url2=url+"&s="+str(j)
            print url2
            # filename=filenames[i]
            # finalhtmls.append(call_agent(url))
            html = call_agent(url)
            print "The html is returned and the size is:", len(html)
            soup = BeautifulSoup(html, "html.parser")# "lxml")
            rows = soup.findAll("p", {"class":"row"})
            if len(rows)>0:
                lastrowdate = rows[-1].time["datetime"]
            else: 
                print "No row in the html page"
                break

            sid = str(lastrowdate)
            sid = sid.replace('-', '')
            sid = sid.replace(':','')
            sid = sid.replace(' ', '')
            df = convertrowstodf(rows, sections[i], sectionlastdate)
            # df['section'] = sections[i]
            # DIV = 1000000
            df = df[df['hashid'] >= sectionlastdate*DIV]
            if df.shape[0]>0:
                # print df.head()
                dataframes.append(df)
            else: 
                print "No row was newer thatn the last section row in database : ", df['hashid'], sectionlastdate*DIV
                break 

            if int(sid)<=sectionlastdate:
                print "The last row is older than the section last update in database : %d > %d"%(int(sid), sectionlastdate) 
                break
             # if not didit:
            #     break
            j+=100

    # print dataframes.head()
    # alldfs=pd.concat(dataframes).sort_values(by=["created_at"], ascending=0)
    # n=alldfs.shape[0]
    # alldfs=alldfs.set_index([range(n)])
    # alldfs=add_broker(alldfs)
    # # updateduplicates()
    # dfdict = alldfs.to_dict(orient='records')
    # # dfdict = [d for d in dfdict if d
    # for dic in dfdict: 
    #     if len(Join.objects.filter(hashid = dic['hashid']))>0:
    #         continue

    #     clean_dict = {k: dic[k] for k in dic if isinstance(dic[k], basestring) or str(dic[k]).isdigit()}
    #     clean_dict.update({k: dic[k] for k in dic if isinstance(dic[k], float) and not isnan(dic[k])})
    #     if 'hashid' in clean_dict:
    # 	# print dic
    #     	a=Join(**clean_dict)
    #     	a.save()
    #     else: 
    #         print clean_dict

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

    print "This is the clean dict: ", clean_dict

    if 'listing_type_text' in clean_dict:
        a.listing_type_text = clean_dict['listing_type_text']
    if 'name' in clean_dict:
        a.name = clean_dict['name']
    if 'email' in clean_dict:
        a.email = clean_dict['email']
    if 'neighborhood' in clean_dict:
        a.neighborhood = clean_dict['neighborhood']
    if 'bedroom' in clean_dict:
        a.bedroom = clean_dict['bedroom']
    if 'bathroom' in clean_dict:
        a.bathroom = clean_dict['bathroom']

    a.save()


def updateneighbors():
    source = []
    areas = []
    nids = []
    parentareas = []

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


    neighb={"area": areas, "parentarea": parentareas, "nid": nids, "source": source}
    df_neighbors=pd.DataFrame(neighb)

    dfdict = df_neighbors.to_dict(orient='records')
    # dfdict = [d for d in dfdict if d
    for dic in dfdict: 
        existing = Neighborhood.objects.filter(source = dic['source'], nid = dic['nid'])
        if len(existing)>0:
            existing.delete()

        clean_dict = {k: dic[k] for k in dic if dic[k]}
        a=Neighborhood(**clean_dict)
        try:
            a.save()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))


def name_similarity(rname, sname): # real name vs similar name 
    N=len(rname)
    Ns=[]
    shift=[-1,0,1]
    accuracy=[]
#     print rname, sname 
    for i in range(len(shift)):
        sh=shift[i]
        if sh<0:
            sn=sname[:sh]
        elif sh>0:
            sn=sname[sh:]
        else:
            sn=sname

        Ns.append(0.)
        for i in range(min(N, len(sn))): 
            if sn[i] == rname[i]: 
                Ns[-1]+=1

        accuracy.append(Ns[-1]/N)
    
    return max(accuracy)
            
    
def match_address(w, adrs): 
    webdict={2:'streeteasy', 3:'nybits', 4:'nakedapartments'}
    adrs=adrs.lower()
    p=0.5
    # 2 is streeteasy, 3 is nybits, and 4 is nakedapartments
    if w<=4 and w>=1:
        neighbordata = Neighborhood.objects.filter(source = webdict[w])
        neighbNames=[n.area for n in neighbordata]
        print neighbNames
        nameDict={}
        for n in neighbNames:
            nameDict[n]=name_similarity(adrs, n)        

        sortedNeighbs=sorted(neighbNames, key=lambda x: nameDict[x], reverse=True) 
        if sortedNeighbs: 
        #             print w, nameDict[sortedNeighbs[0]], sortedNeighbs[0:2]
            theneighbor = neighbordata.get(area = sortedNeighbs[0])
            if nameDict[sortedNeighbs[0]]>p:
                return (theneighbor.parentarea, theneighbor.area, theneighbor.nid)
            else: 
                return (-1,-1,-1)
        else: 
            return (-1,-1,-1)
    
    else: 
        return (-1,-1,-1)
        

def retrieve_hidden(w, soup, getVars):
    if w == 'nybits':
        form=soup.find('form', {'name':'sform'})
        input_hidden_values=form.find_all('input', {'type':'hidden'})
        for inp in input_hidden_values: 
            getVars[inp.get('name')]= inp.get('value')
    
    return getVars
    

def retrieve_beds(w, getVars, beds): 
    if w == 'streeteasy':
        getVars["beds"] = beds
    elif w == 'nybits': 
        dic = {1:"1br", 2:"2br", "loft":"loft", 3:"3more", 4:"3more", "studio":"studio"}
        getVars["!!atypes"] =  dic[beds]
        
    # elif w == 'nakedapartments': 
    #     nakeddict={0:"1", "studio":"1", 1:"3", 2:"4", 4:"6", "room":"11", "loft": "2"}
    #     getVars["aids"]=nakeddict[beds]
    
    # if w == 'nybits': 
    #     getVars["bedrooms"]=beds
        
    return getVars

def retrieve_baths(w, getVars, baths): 
    if baths:
        if w == 'nybits': 
            getVars["baths"]=round(baths)
        elif w == 'nakedapartments':
            getVars["bathrooms"]=int(baths)
            
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
        if m[2]>0:
            getVars["nids"]=m[2]
    
    # elif w == 'nakedapartments': 
    #     m=match_address(w, address)
    #     if m[2]::
    #         getVars["query"]=m[2]
        
    return getVars

def retrieve_price(w, soup, getVars, pricemin, pricemax):
    if w == 'nybits':
        form=soup.find('select', {'name':'!!rmin'})
        options=form.find_all('option')
        minprices=['0']
        for inp in options: 
            minprices.append(inp.get('value'))

        minprices=[int(p) for p in minprices if p.isdigit()]
        minp=min(minprices, key=lambda x:abs(x-pricemin))
        getVars['!!rmin']=minp

        form=soup.find('select', {'name':'!!rmax'})
        options=form.find_all('option')
        maxprices=[]
        for inp in options: 
            maxprices.append(inp.get('value'))

        maxprices=[int(p) for p in maxprices if p.isdigit()]
        maxp=min(maxprices, key=lambda x:abs(x-pricemax))
        getVars['!!rmax']=maxp
    
    elif w == 'nakedapartments': 
        getVars['min_rent']=pricemin
        getVars['max_rent']=pricemax
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


def calhashid(beds, neighborhood, address, price, source): 
# beds is a string, price is a integer number and source is a string 
    sourcenum = {'streeteasy': 2, 'nybits': 3, 'nakedapartments':4, 'craigslist': 1}
    bedsdict = {'studio': '8', 'loft': '9'}


    sid=str(sourcenum[source])

    if beds:
        beds = str(beds)
        if beds.isdigit():
            sid += beds.zfill(1)[:1]
        else: 
            sid += bedsdict[beds]
    else:
        sid += '0'
    
    nlength = 0
    nparts = 0
    naddress = 0

    if neighborhood:
        neighborhood = neighborhood.strip()
        nlength = len(neighborhood)
        nparts = len(neighborhood.split())
    
    if address:
        address = address.strip()
        naddress = len(address)
        
    temptext='0000'
    if nlength > 0: 
        temp=sum([ord(s) for s in neighborhood])
        temptext = str(nlength+nparts+naddress+temp).zfill(4)[:4]

    sid+=temptext
        
    
    if isinstance(price,float) or (price is None):
        sid+='00'
    else: 
        sid += str(round(price/100.)).zfill(2)[:2]
    
    # print temptext, price, naddress, nlength, sid
    return int(sid)



def url2db(urls): 
    sourcedict = {'http://www.nakedapartments.com/': 'nakedapartments' , 'http://www.nybits.com/': 'nybits',  'http://streeteasy.com/': 'streeteasy'}
    prices = []
    addresses = []
    neighborhoods = [] 
    imagelinks = []
    urllinks = []
    beds = []
    baths = []
    ft2s = []
    sourcepages = []
    hashids = []
    created_at = []

    for url in urls:
        baseURL = re.match(r'\w+://(.+\.\w+)/', url).group(0)
        if baseURL not in sourcedict:
            return False

        print url 
        html = call_agent(url)
        soup = BeautifulSoup(html, "html.parser")
        w = sourcedict[baseURL]
        if w == 'streeteasy':
            rows = soup.findAll("div", {"class":'item'})
            for row in rows: 
                urllinks.append(baseURL+row.find("div", {"class": "details-title"}).find("a")["href"])
                tempprice = re.match(r'\$(\d+),(\d{3})', row.find("span", {"class": "price"}).text)
                prices.append(int(tempprice.group(1)+tempprice.group(2)))
            #     prices.append(row.find("span", {"class": "price"}).text)
                imagelinks.append(row.find(attrs = {"class": "lazy"})["data-original"])
                addresses.append(row.find(attrs = {"class": "details-title"}).find("a").text.split(' #')[0])
                details = row.findAll(attrs = {"class":  'details_info'})
                sizeinfo = details[0].text
                neighbtext = re.sub('\s+', ' ', details[1].text)
                neighb = re.match(r'.+Rental Unit in (.*)', neighbtext)
                if neighb: 
                    temp = neighb.groups(1)[0]        
                    neighborhoods.append(temp)
                else:
                    neighborhoods.append('')

                
                snums= re.findall(r'(\d+)', sizeinfo)
                n = len(snums)
                if n>=1:
                    beds.append(int(snums[0]))
                    if n>=2:
                        baths.append(int(snums[1]))
                        if n>2:
                            ft2s.append(int(snums[2]))
                        else: 
                            ft2s.append(None)
                    else:
                        baths.append(None)
                else: 
                    beds.append(None)
                    
                sourcepages.append(w) 
                SID = calhashid(beds[-1], neighborhoods[-1], addresses[-1], prices[-1], w)
                DT = currentdatetimestring()
                hashids.append(SID)
                created_at.append(DT)

            # print "After streeteasy:", len(prices), len(baths)


        elif w == 'nybits':
            table = soup.find("table", {"id": "rentaltable"})
            rows = table.findAll("tr")

            tempaddresses = []
            tempimagelinks = []
            tempprices = []
            tempbeds = []
            tempneighborhood = []
            tempbedroom = []
            tempurllinks = []
            n = 3
            i=0
            for row in rows:
                if i>=n: 
                    break
                firtcolumn = row.find("td", {"class": "lst_sr_price"})
                if (not firtcolumn) or (len(firtcolumn.text)==0): 
                    continue
                secondcolumn = row.find("td", {"class": "lst_sr_topcell"})
                if not secondcolumn:
                    continue
                featureimage = secondcolumn.find("img")
            #     print featureimage
                if featureimage: 
                    i+=1
                    url = secondcolumn.find("a")["href"]
                    tempurllinks.append(url)
                    pricetext =  firtcolumn.text.replace('\n', '')
                    # print "this is the first column: ", pricetext
                    pricestring = re.match(r'.*\$(\d+),(\d{3})', pricetext) 
                    tempprices.append(int(pricestring.group(1)+pricestring.group(2)))
                    html = call_agent(url)
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.find("div", {"id": "dancefloor"}).find('h1').text
                    bedroom = re.match(r'(\d).Bedroom', title).group(1)
                    tempbedroom.append(int(bedroom))



                    content = soup.find("div", {"class": "listing_content"})
                    tempimagelinks.append(content.find("img")["src"])
                    table = soup.find("table", {"class": "listing_summary"})
                    rows = table.findAll("tr")
                    for row in rows: 
                        columns = row.findAll("td")
                        if "Building" in columns[0].text:
                            tempaddresses.append(columns[1].text.replace('\n', ''))
                            continue
                        elif "Neighborhood" in columns[0].text:
                            tempneighb = columns[1].text.replace('\n', '')
                            neigb = tempneighb.split(';')[-1]
                            tempneighborhood.append(neigb)
                    

                    SID = calhashid(tempbedroom[-1], tempneighborhood[-1], tempaddresses[-1], tempprices[-1], w)
                    DT = currentdatetimestring()
                    hashids.append(SID)
                    created_at.append(DT)
                    baths.append(None)
                    ft2s.append(None)
                    sourcepages.append(w)

            prices += tempprices
            addresses += tempaddresses
            neighborhoods += tempneighborhood
            imagelinks += tempimagelinks
            urllinks += tempurllinks
            beds += tempbedroom

            # for i in range(len(tempprices)):
            #     baths.append(None)
            #     ft2s.append(None)
            #     sourcepages.append('nybits')

            # print "After nybits:", len(prices), len(baths)


        elif w == 'nakedapartments':
            rows = soup.findAll("div", {"class":"listing-row listing-row-standard  mappable-element ab-test mobile-web-style row"})


            for row in rows: 
                rowimage = row.find(attrs = {"class": "lazy"})["data-original"]
                imagelinks.append(rowimage)
            #     print "imagelink:", rowimage["data-original"]
                rowinfo = row.find(attrs = {"class": "listing-details col-xs-8"})
                # print "Row info is:", rowinfo
                listingtitle = rowinfo.find(attrs={"class": "listing-title"})
            #     print listingtitle.text
            #     print listingtitle.text
                tempprice = re.match(r'\$(\d+),(\d{3})', listingtitle.text)
                prices.append(int(tempprice.group(1)+tempprice.group(2)))
                urllinks.append(listingtitle['href'])
                listingaddress = rowinfo.find(attrs={"class": "listing-address"})
                sizeinfo = rowinfo.find("span", {"class": "listing-size"}).text
                # print "Size info is :", sizeinfo
                bedsbaths = re.match(r'(\d)br, (\d?.?\d)ba', sizeinfo.lower())
                if bedsbaths:
                    beds.append(int(bedsbaths.group(1)))
                    baths.append(int(bedsbaths.group(2)))
                else:
                    beds.append(sizeinfo.lower())
                    baths.append(None)

                addresses.append(listingaddress.text)
            #     print listingaddress.text
                listingneighb = rowinfo.find(attrs = {"class": "listing-neighborhood"})
                neighborhoods.append(listingneighb.text)
                ft2s.append(None)
                sourcepages.append(w) 
                
                #beds, neighborhood, address, price, source,
                SID = calhashid(beds[-1], neighborhoods[-1], addresses[-1], prices[-1], w)
                DT = currentdatetimestring()
                hashids.append(SID)
                created_at.append(DT)

            # print "After nakedapartments: ", len(prices), len(baths)




        print len(addresses), len(beds), len(prices), len(baths), len(imagelinks), len(neighborhoods), len(urllinks), len(ft2s), len(sourcepages), len(created_at)
        finaldict = {'hashid': hashids,'full_address': addresses, 'bedroom':beds, 'price': prices, 'bathroom': baths, 'image_url': imagelinks, 'neighborhood': neighborhoods, 'linkurl': urllinks, 'source': sourcepages, 'created_at': created_at}
        df = pd.DataFrame(finaldict)
        dfdict = df.to_dict(orient='records')
        # dfdict = [d for d in dfdict if d
        for dic in dfdict: 
            if len(Join.objects.filter(hashid = dic['hashid']))>0:
                a = Join.objects.filter(hashid = dic['hashid'])
                a.delete()

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



def create_url(address='nyc', pricemin=0, pricemax=20000, beds=1, baths=1, fee=0):
    urls = []
    sources = ['streeteasy', 'nakedapartments']
    for w in sources:
        if w == 'streeteasy':
            m=match_address(w, address)
            if m[0]>0: 
                urladdress="http://streeteasy.com/for-rent/"+m[1].replace(' ', '-')
            else:
                urladdress="http://streeteasy.com/for-rent/nyc"
                
            urladdress=urladdress+"/price:%s-%s"%(pricemin, pricemax)
            urladdress=urladdress+"%7"+"Cno_fee:%d"%fee
            urladdress=urladdress+"%7"+"Cbeds=%d"%beds
            urls.append(urladdress)
        
        elif w == 'nybits':
            url="http://www.nybits.com/search/"
            # filename=re.search("://.+\.\w+/", url).group(0).replace('.','_')[3:-1]#.replace(':','').replace('/','')
            #save_html(url, filename)
            # filepwd="Files/%s.html"%filename
            # html=codecs.open(filepwd)
            html = call_agent(url)
            soup = BeautifulSoup(html, "html.parser")
            getVars={'orderby':'dateposted'}
            getVars=retrieve_hidden(w, soup, getVars)
            getVars=retrieve_beds(w, getVars, beds)
            if address != 'nyc':
                getVars=retrieve_address(w, address, getVars)

            getVars=retrieve_price(w, soup, getVars, pricemin, pricemax)
            getVars = retrieve_fee(w, getVars)
            print "This is the nybits variables:", getVars
            urls.append(url + "?"+urllib.urlencode(getVars))
        
        elif w == 'nakedapartments':
            url="http://www.nakedapartments.com/"
            #save_html(url, filename)
            html = call_agent(url)
            soup = BeautifulSoup(html, "html.parser")
    #         retrieve_neighborhoods(w, soup, 'www_nakedapartments_com', 'neighborhood_nakedapartments')
            getVars={}
            getVars=retrieve_beds(w, getVars, beds)
            if address != 'nyc':
                getVars=retrieve_address(w, address, getVars)

            getVars=retrieve_baths(w, getVars, baths )
            getVars=retrieve_price(w, soup, getVars, pricemin, pricemax)
            urls.append(url + "renter/listings/search?"+urllib.urlencode(getVars))

    url2db(urls)
    return urls



def sendrequesttoanni():
    url = "https://boiling-eyrie-43826.herokuapp.com/webhook?query=test"
    html = call_agent(url)
    print html

    


#     elif w == 'nybits': 
#         url="http://newyork.craigslist.org/search/abo"
#         filename=re.search("://.+\.\w+/", url).group(0).replace('.','_')[3:-1]#.replace(':','').replace('/','')
#         #save_html(url, filename)
#         save_ny_neighbor_words()
# #         filepwd="Files/%s.html"%filename
# #         html=codecs.open(filepwd)
# #         soup = BeautifulSoup(html, "lxml")
# #         retrieve_neighborhoods(w, soup, 'www_nakedapartments_com', 'neighborhood_nakedapartments')
#         getVars={}
#         getVars=retrieve_beds(w, getVars, beds)
#         getVars=retrieve_address(w, address, getVars)
#         getVars=retrieve_baths(w, getVars, baths )
#         getVars=retrieve_price(w,'', getVars, pricemin, pricemax)
#         return url+"?"+urllib.urlencode(getVars)







