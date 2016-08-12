import sys,base64, os 

#=====================Running Django code locally=========================
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newworld.settings")
application = get_wsgi_application()
#========================================================================

import joins.scodes as scodes


# neighs = ['Brooklyn']

scodes.updatejoinery()

neighs = ['Williamsburg', 'Bushwick','Greenpoint','Clinton Hill','Brooklyn Heights','Boerum Hill','Cobble Hill','Carrol Gardens','DUMBO', 'Prospect Heights',\
'Gowanus','Crown Heights','Bedford-Stuyvesant','Sunset Park','East Village','Lower East Side','SoHo','West Village','Tribeca','Harlem','Flatiron','Chelsea','Hells Kitchen',\
'Upper East Side','Morningside',' Heights','Astoria','Flushing','Queens','Brooklyn','Manhattan','Bronx']
scodes.create_JSurl(neighs)
scodes.updateaddresscoordinates()
scodes.updatebedsbaths() 
