import pathlib
import pydash
import ssl
from suds.client import Client
from suds.xsd.doctor import Import
from suds.xsd.doctor import ImportDoctor

axlpath = '/Code/py-axl/AXLAPI.wsdl'
axluri = pathlib.Path(axlpath).as_uri()

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

axlwsdl = axluri
axllocation = 'https://1.2.3.4:8443/axl/'

username = 'axladmin'
password = 'axlpass'

tns = 'http://schemas.cisco.com/ast/soap/'
imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add(tns)

axl = Client(axlwsdl,location=axllocation,faults=False,plugins=[ImportDoctor(imp)],
                username=username,password=password)
                
def getSubs():
    res = axl.service.listProcessNode({'name': '%', 'processNodeRole': 'CUCM Voice/Video'}, returnedTags={'name': ''})
    subs = res[1]['return']['processNode']
    for sub in subs:
        if sub.name != 'EnterpriseWideData':
            print(sub.name)

def listPhones():
    res = axl.service.listPhone({'name': '%'}, returnedTags={'name': ''})
    if res[1]['return']:
        phones = res[1]['return']['phone']
        for phone in phones:
            if phone.name.startswith('SEP'): 
                print(phone.name)


getSubs()
listPhones()
