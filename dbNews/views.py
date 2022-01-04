from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import operator
import time
import uuid
from datetime import datetime
from decimal import Decimal
import requests

from operator import itemgetter

from io import StringIO
import io
import base64
import urllib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    newslist=[]
    searchcriteria=None
    dbData=dbPull()
    newsdf=pd.DataFrame(dbData[0])
    mktdata=dbData[1]

    newsdf['id']=newsdf['_id']
    newsdf=newsdf.sort_values(by=['Published'],ascending=False)
    newslist=newsdf.to_dict('records')
    rendering={'newslist':newslist,'mktdata':mktdata}
    
    return render(request, 'newhome.html',rendering)
    

def nsetopgainers():
    return nse_get_top_gainers()[['symbol','lastPrice','pChange']].to_dict('records')
    
def nsetoplosers():
    return nse_get_top_losers()[['symbol','lastPrice','pChange']].to_dict('records')


@api_view(['GET'])
def dbPull(request):
    import urllib
    import pymongo
    url = "mongodb+srv://vladha:"+urllib.parse.quote("Energy123")+"@cluster0.ju4zq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    myclient = pymongo.MongoClient(url,tls=True, tlsAllowInvalidCertificates=True)

    mydb = myclient["news"]
    feedcol = mydb["feed"]
    mktcol = mydb["markets"]


    all=list(feedcol.find({}))
    mktdata=list(mktcol.find({}).sort('_id',-1).limit(1))[0].get('markets')
    for keys in mktdata:
        dict=mktdata.get(keys)
        dict['disp']=str(dict.get('last'))+" ("+str(dict.get('percChange'))+")"


    
    return Response({'all':all,'mktdata':mktdata})


