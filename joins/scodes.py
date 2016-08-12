from .models import Join, Neighborhood, Userhist
from django.db.models import Q
import urllib2

from bs4 import BeautifulSoup
# import codecs
import urllib
import datetime 
from codes import * 


def updatebedsbaths(): 
    a = Join.objects.all()
    for e in a:
        if e.title:
            beds, baths = codes.updatebedsbaths(e)
            e.bedrooms = beds
            e.bathrooms = baths
            print e.title, beds, baths
            e.save()

def updatelatlng(l): 
    lat = None
    lng = None 
    print l.latitude, l.longitude,
    if (not (l.latitude and l.longitude)) or l.latitude == l.longitude: 
        n = l.neighborhood if l.neighborhood else ''
        pn = l.parent_neighborhood if l.parent_neighborhood else ''
        a = l.full_address if l.full_address else ''
        dic = {"address": a + " " + n + " "+ pn + " NY"}
        print dic["address"]
        url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(dic)
        try:
            response = urllib2.urlopen(url)
            data = json.load(response) 
            if "results" in data:
                # results =  data[""]
                lat = data["results"][0]["geometry"]['location']['lat'] 
                lng = data["results"][0]["geometry"]['location']['lng']
        except: 
            print "Failed query"

    else: 
        lat = l.latitude
        lng = l.longitude

    return (lat, lng)



def updateaddresscoordinates(): 
    listings = Join.objects.all().order_by('-created_at')
    i = 0
    for l in listings:
        i+=1
        if i>2500:
            break 

        lat, lng = updatelatlng(l)
        print lat, lng
        l.latitude = lat
        l.longitude = lng
        l.save()

        # if not (l.latitude and l.longitude): 
        #     n = l.neighborhood if l.neighborhood else ''
        #     pn = l.parent_neighborhood if l.parent_neighborhood else ''
        #     a = l.full_address if l.full_address else ''
        #     dic = {"address": a + " " + n + " "+ pn + " NY"}
        #     print dic["address"]
        #     url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(dic)
        #     try:
        #         time.sleep(0.04)
        #         response = urllib2.urlopen(url)
        #         data = json.load(response) 
        #         if "results" in data:
        #             # results =  data[""]
        #             lat = data["results"][0]["geometry"]['location']['lat'] 
        #             lng = data["results"][0]["geometry"]['location']['lng']

        #             print lat, lng
        #             l.latitude = lat
        #             l.longitude = lng
        #             print "SUCCESS"
        #             l.save()

        #         else: 
        #             parent, neighb, = matchallneighbor(n) if len(n)>0 else None
        #             if neighb: 
        #                 b = Neighborhood.objects.filter(area = neighb)[0]
        #                 l.latitude = b.latitude
        #                 l.longitude = b.longitude
        #                 print "No Query"
        #                 l.save()

        #     except: 
        #         print "Failed Try!"
        #         continue


def updatejoinery(): 
    url = "https://joinery.nyc/api/v1/listings/available"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    SIDs = []
    try: 
        a = Join.objects.filter(source = 'joinery')
        # print len(a)
        print "All prevoius joinery listings are removed"

    except: 
        print "Cannot remove the joijnery listings"

    for i in range(len(data)):
        l = data[i] 
        l["tag"] = 'listing'
        # print l["parent_neighborhood"], type(l['parent_neighborhood'])
        l["parent_neighborhood"] =l["parent_neighborhood"]["name"] if "name" in l["parent_neighborhood"] else None

        sid = saveuserdata(l)
        if sid in SIDs: 
            print l, sid
            print ''
        else: 
            SIDs.append(sid)

            
def scrapeWithPhantom(urls):
    start_time = datetime.datetime.now()
    for url in urls:
        sourcedict = { 'http://www.zumper.com/' : 'zumper'}
        dfdict = [] # the array of dictionaries 
        titles = []
        prices = []
        addresses = []
        neighborhoods = [] 
        pneighborhoods = []
        imagelinks = []
        urllinks  = []
        beds = []
        baths = []
        ft2s = []
        sourcepages = []
        hashids = []
        created_at = []
        score = []
        
        neighbd = Neighborhood.objects.all()
        
        baseURL = re.match(r'\w+://(.+\.\w+)/', url).group(0)
        if baseURL not in sourcedict:
            return False
        soup = call_agent(url)
        
        w = sourcedict[baseURL]
        if w == 'zumper':
           
            apt_info = soup.find_all('div',{'class':"feedItem-details"})
            imgs = soup.find_all('img', {'class':"feedItem-img ng-isolate-scope"})
            imgList = [x['src'] for x in imgs]
            if not apt_info or not imgs:
                print 'Try again later'
            for apt, img in zip(apt_info, imgList):
                    #print apt.find_all('span', {'ng-bind':"item.getBedsBathsText()"})
                address = apt.find_all('a')[0].text
                addresses.append(address)
                current_url = baseURL + apt.find_all('a', href=True)[0]['href'][1:]
                urllinks.append(current_url)
                n = apt.find('a', {'class':"feedItem-hoodLink"}).text
                neighborhood =  n[n.index('More')+len('More'):n.index('apartments')]
                neighborhoods.append(neighborhood)
                neighborhood = neighborhood.strip()
                n = neighbd.filter(area = neighborhood)


                if n:
                    n = n[0]
                    pneighborhoods.append(n.parentarea)
                else:
                   pneighborhoods.append(None)

                pricebedbathlist = apt.find_all('p')[0].text
                pricebedbath = re.match(r'\s+\$(\d+)?,?(\d+)?\s+\|\s*(\d)\sbed.*\s(\d?.\d?)\sbath.*\s+', pricebedbathlist.lower())
                price = 0
                bed = '0'
                bath = 0

                if pricebedbath:
                    if pricebedbath.group(2):
                        price = int(pricebedbath.group(1)+pricebedbath.group(2))
                        bed = str(pricebedbath.group(3))
                        bath = int(pricebedbath.group(4)) 
                    else:
                        price = int(pricebedbath.group(1))
                        bed = str(pricebedbath.group(2))
                        bath = int(pricebedbath.group(3)) 
                else:
                    print('Not Apartment \n Price, Bed, Bath Unknown:')
                    continue

                prices.append(price)
                beds.append(bed)
                baths.append(bath)
                img_url = img
                imagelinks.append(img_url)
                DT = currentdatetimestring()
                created_at.append(DT)
                SID = calhashid(bed, neighborhood, address, price, w)
                hashids.append(SID)

                sourcepages.append(w)

                title = address + pricebedbathlist
                titles.append(title)
                print "Title: %s" % title
                print "URL: %s" % current_url
                print "Address: %s" %address
                print 'Parent Neighbothood: %s' % pneighborhoods[-1]
                print "Neighborhood: %s" %neighborhood
                print "Price: %d" %price
                print "Beds: %s" %bed
                print "Baths: %d" %bath
                print "Created at: %s" %DT
                print "img_link: %s" %img_url
                print "Hash id: %s" %SID
                print ""
                dfdict.append({'hashid': hashids[-1],'full_address': addresses[-1], 'bedrooms':beds[-1], 'price': prices[-1], 'bathrooms': baths[-1], 'image_url': imagelinks[-1], 'neighborhood': neighborhoods[-1], 'url': urllinks[-1], 'source': 'zumper', 'created_at': created_at[-1], 'parent_neighborhood': pneighborhoods[-1], 'title' : titles[-1]})
                print("--- %s seconds ---" % (datetime.datetime.now() - start_time))
    hashidlist = [d['hashid'] for d in dfdict]
    N = len(dfdict)
    print "The unique number of hashids:", set(hashidlist)
    hash2dblist = []
    for dic in dfdict: 
        if len(Join.objects.filter(hashid = dic['hashid']))>0:
            hashidlist.remove(dic['hashid'])
            a = Join.objects.filter(hashid = dic['hashid'])
            dic['created_at'] = a[0].created_at
            a.delete()

        clean_dict = {k: dic[k] for k in dic if isinstance(dic[k], basestring) or str(dic[k]).isdigit()}
        clean_dict.update({k: dic[k] for k in dic if isinstance(dic[k], float) and not isnan(dic[k])})
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
    print w
    return (hash2dblist, N)

    

def create_JSurl(neighList):
    start_time = datetime.datetime.now()
    pricemin=0
    pricemax=5000
    beds='1'
    baths=1
    urls = []
    sources = ['zumper']
    
    for n in neighList:
        address = n
        for w in sources:
            if w == 'zumper':
                address = address.replace(' ','%20')
                print address
                url = 'http://www.zumper.com/apartments-for-rent/new-york-ny/%s/no-fee/%s-beds/price-%s,%s?property-categories=apartment' % (address, beds,pricemin,pricemax)
                print url
                wait = "subnav-view-toggle"
                soup = call_agent(url, wait = wait)
                loc_url = soup.find_all('div', {'class':"subnav-view-toggle"})[0].find_all('a')[1]['href']
                box = loc_url.find('?box')
                print box
                #check if neighborhood passes a box value. If it does, passes it into latlng.
                if box != -1:
                    latlng = loc_url[box:]
                    url = 'http://www.zumper.com/apartments-for-rent/new-york-ny/no-fee/%s-beds/price-%s,%s%s&property-categories=apartment'%(beds, pricemin,pricemax,latlng)
                    #soup = call_agent(url)
                #pages = soup.find('div',{'class': "results-count"}).text
                #p = re.findall(r'\d+', pages)
               # if not p:
                #    print('Try Zumper Later')
                urls.append(url)
                # else:
                #     pages = int(re.findall(r'\d+', pages)[0])
                #     #print pages
                #     pageCount = (pages / 10) + 1
                #     print 'Result returned this many pages: ' + str(pageCount)
                #     for i in xrange(pageCount):
                #             urls.append(url+'&pages='+str(i+1))
                print 'Finished url for %s : %s' % (n, url)
            
    print 'It took this %s seconds' % (datetime.datetime.now() - start_time)
    print urls
    print scrapeWithPhantom(urls)