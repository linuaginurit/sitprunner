from django.shortcuts import render
from pandas.io.json import json_normalize
import urllib3
import requests
import datetime
import pandas as pd
import numpy as np
import json
from operator import itemgetter


# Create your views here.
def convert(distance):
  return round(float(distance)/1000, 2)
def index(request):
  auth_url = "https://www.strava.com/oauth/token"
  activites_url = "https://www.strava.com/api/v3/clubs/1066758/activities"
  payload = {
      'client_id': "91910",
      'client_secret': 'f21c37bd426d253320db0b3dadeec2530cc207c0',
      'refresh_token': '2b78f9b2cf0721d250def8bb86051173f8daabd6',
      'grant_type': "refresh_token",
      'f': 'json'
  }

  print("Requesting Token...\n")
  res = requests.post(auth_url, data=payload, verify=False)
  access_token = res.json()['access_token']
  print("Access Token = {}\n".format(access_token))



  header = {'Authorization': 'Bearer ' + access_token}
  param = {'per_page': 9, 'page': 1}
  my_dataset = requests.get(activites_url, headers=header, params=param).json()
  df=json_normalize(my_dataset)
  print(my_dataset)
  # print(df)/
  group=df.groupby(['athlete.firstname'])['distance'].sum()
  group2=df.groupby(['athlete.firstname'])['distance'].count()
  # print(group2)
  json_records = group.reset_index().to_json(orient ='records') 
  data = [] 
  data = json.loads(json_records) 
  # print(list(data))
  dfjson=pd.DataFrame(data)
  dfjson['km']=dfjson.apply(lambda row: convert(row['distance']), axis=1)
  dfjson.rename(columns = {'athlete.firstname':'firstname'}, inplace = True)
  print(dfjson)
  json_records2 = dfjson.reset_index().to_json(orient ='records') 
  data2 = [] 
  data2 = json.loads(json_records2)
  data2.sort(key = itemgetter('distance'), reverse=True)
  
  context={
    'responses':data2
  }
  return render(request,'index.html',context)