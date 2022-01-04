#from azure.cognitiveservices.search.imagesearch import ImageSearchClient
#from msrest.authentication import CognitiveServicesCredentials

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# You may need the below as well
# pip install pipenv
# pipenv install requests
# <importsAndVars>
import json
import os
from pprint import pprint
import requests 

'''
This sample uses the Bing Custom Search API to search for a query topic and get back user-controlled web page results.
Bing Custom Search API: https://docs.microsoft.com/en-us/bing/search-apis/bing-custom-search/overview 
'''

# Add your Bing Custom Search subscription key and endpoint to your environment variables.
subscriptionKey = "e3f606ef2acc4d088c541a9ae5ea740d"
endpoint = "https://api.bing.microsoft.com/v7.0/custom/images/search"
customConfigId = "d2867c4c-d99b-4ae7-b21c-5e1e18bd6aab"  # you can also use "1"
searchTerm = "Stan Lee organização de censura da indústria"
# </importsAndVars>
# <url>
# Add your Bing Custom Search endpoint to your environment variables.
#url = endpoint + "/bingcustomsearch/v7.0/search?q=" + searchTerm + "&customconfig=" + customConfigId
url = endpoint + "?q=" + searchTerm + "&count=5&customconfig=" + customConfigId
# </url>
# <request>
r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': subscriptionKey})
pprint(json.loads(r.text))
# </request>