"""AXL <addLine> sample script, using the SUDS-Jurko library

Script Dependencies:
    suds
    logging (optional)

Depencency Installation:
    $ pip install suds-jurko

Copyright (c) 2018 Cisco and/or its affiliates

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Installing a root/CA Certificate
# (Tested on Ubuntu Linux 18.04)

# Retrieve certificate from target CUCM host
#     - openssl s_client -showcerts -connect cucm-node.example.com:443 </dev/null 2>/dev/null|openssl x509 >cucm-node.example.com.crt
# Store certificate on the client
#     - Create a directory for extra CA certificates in /usr/share/ca-certificates:
#        sudo mkdir /usr/share/ca-certificates/extra
#     - Copy the CA .crt file to this directory:
#        sudo cp foo.crt /usr/share/ca-certificates/extra/foo.crt
#     - Append the certificate path (relative to /usr/share/ca-certificates) to /etc/ca-certificates.conf
#        sudo dpkg-reconfigure ca-certificates
#
# In case of a .pem file, it must first be converted to a .crt file:
#     openssl x509 -in foo.pem -inform PEM -out foo.crt

import os
import sys

# Get the absolute path for the project root
project_root = os.path.abspath(os.path.dirname(__file__))

# Extend the system path to include the project root and import the env file
sys.path.insert(0, project_root)
import user_env

# Uncomment the next 3 lines to enable detailed logging
# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("suds.transport").setLevel(logging.DEBUG)

from suds.client import Client

client = Client("file://"+user_env.WSDL_PATH,
                location="https://"+user_env.CUCM_LOCATION+"/axl/",
                username=user_env.CUCM_USER,
                password=user_env.CUCM_PASSWORD)

newLine = {
            "pattern": "5555",
            "routePartitionName": ""
            }

result = client.service.addLine(newLine)

ean = {
    "numMask": "8XXXX",
    "isUrgent": True,
    "addLocalRoutePartition": True,
    "routePartition": "testPartition"
}

cfa = {
    "callingSearchSpaceName": "Test_CSS",
    "secondaryCallingSearchSpaceName": None,
    "destination": "9999"
    }

result = client.service.updateLine(
    pattern = "5555",
    routePartitionName = "",
    description = "test description",
    useEnterpriseAltNum = True,
    enterpriseAltNum = ean,
    callForwardAll = cfa
)

print(result)
