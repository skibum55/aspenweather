from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from influxdb import DataFrameClient

#get pages
pages =['http://weather.aspensnowmass.com/aspen-summary.htm','http://weather.aspensnowmass.com/snowmass-summary.htm','http://weather.aspensnowmass.com/highlands-summary.htm','http://weather.aspensnowmass.com/buttermilk-summary.htm']
for i in pages:
  # address = 'http://weather.aspensnowmass.com/highlands-summary.htm'
#  response = urllib.request.urlopen(address)
  response = urllib.request.urlopen(i)
  html = response.read()

  #parse page
  soup = BeautifulSoup(html,"html.parser")
  table = soup.find("pre").contents[0]
  print(table)

  #write data out http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
  file_name = i.split('/')[-1]
  filename1 = file_name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.htm'
  with open(filename1,'wb') as output:
    output.write(html)

#replace spaces with commas
newtable = re.sub(r"[ \t]+", ',', table)

#make an array
weather_array=newtable.splitlines()

#get rid of headers & footers
divider_index = [i for i, item in enumerate(weather_array) if item.endswith('----')]
new_weather_array=weather_array[divider_index[0]+1:-23]

# header_array=weather_array[3:divider_index[0]]

#create dataframe
Header =['Month','Day','Hour','LogeTempF','LogeRelHum%','LogeAvgWindMPH','LogeMaxWindMPH','LogeWindDirDeg','LogeSurfTempDegF','LogeAvgSolarWM2','LogeMaxSolarWM2','Cloud9AvgTempDegF','Cloud9RelHum%','Cloud9NewSnowIn','Cloud9TotSnowIn','NWoodsTempDegF','NWoodsNewSnowIn','NWoodsTotSnowIn','PeakAvgWindMPH','PeakMaxWindMPH','PeakWindDir','JeromeTempDegF']
new_weather_row = pd.DataFrame(columns=Header)

# http://stackoverflow.com/questions/11833266/how-do-i-read-the-first-line-of-a-string

# split rows from text

# split_weather= [i for i in enumerate(weather_array) weather_array[i].split(“,”)]

for i in range(0, len(new_weather_array)): new_weather_row.append(new_weather_array[i].split(","))

# Faked header creation for the time being TODO Dynamically pull stuff so you can use all the datasets
#Header =['Month','Day','Hour','Loge Temp F','Loge RelHum %','Loge AvgWind MPH','Loge MaxWind MPH','Loge WindDir Deg','Loge SurfTemp Deg F.','Loge AvgSolar W/m2','Loge MaxSolar W/m2','Cloud9 AvgTemp Deg F.','Cloud9 RelHum %','Cloud9 NewSnow in.','Cloud9 TotSnow in.','NWoods Temp Deg F.','NWoods NewSnow in.','NWoods TotSnow in.','Peak AvgWind MPH','Peak MaxWind MPH','Peak WindDir ','Jerome Temp. Deg F.']

# add rows to temporary array, then split and add to data frame
# http://stackoverflow.com/questions/31674557/how-to-append-rows-in-a-pandas-dataframe-in-a-for-loop
tempvar = []
new_weather_row=pd.DataFrame(columns=Header)
for i in range(0, len(new_weather_array)):
    tempvar.append(new_weather_array[i][1:].split(","))
new_weather_row=pd.DataFrame(tempvar, columns=Header)

# convert everything to numeric http://chris.friedline.net/2015-12-15-rutgers/lessons/python2/03-data-types-and-format.html
# mycolumns=new_weather_row.columns
mycolumns=list(new_weather_row.columns)
# new_weather_row.apply(lambda x: pd.to_numeric(x, errors='ignore'))
#new_weather_row.apply(lambda x = None: if x == 'None' else x)
for i in range(0, len(mycolumns)):
    new_weather_row[mycolumns[i]] = new_weather_row[mycolumns[i]].astype('float64')

# http://stackoverflow.com/questions/9223905/python-timestamp-from-day-month-year
# http://stackoverflow.com/questions/33680666/creating-a-new-column-in-panda-by-using-lambda-function-on-two-existing-columns
new_weather_row["timestamp"] = new_weather_row.apply(lambda x: datetime.datetime(year=2017, month=int(x['Month']), day=int(x['Day']),hour=int(int(x['Hour'])/100)-1),axis=1)
# http://stackoverflow.com/questions/30857680/pandas-resampling-error-only-valid-with-datetimeindex-or-periodindex
new_weather_row = new_weather_row.set_index(['timestamp'])
    
#new_weather_row["timestamp"] = new_weather_row.apply(lambda i: datetime.datetime(year=2016, month=int(new_weather_row.loc[i,'Month']), day=int(new_weather_row.loc[i,'Day']),hour=int(int(new_weather_row.loc[i,'Hour'])/100)-1))
   
#   dt=datetime.datetime(year=2016, month=int(new_weather_row.loc[i,'Month']), day=int(new_weather_row.loc[i,'Day']),hour=int(int(new_weather_row.loc[i,'Hour'])/100)-1)
#    dt=datetime.datetime(year=2016, month=int(new_weather_row['Month'][i]), day=int(new_weather_row['Day'][i]),hour=int(new_weather_row['Hour'][i]/100)-1)
#    time.mktime(dt.timetuple())
# http://stackoverflow.com/questions/12555323/adding-new-column-to-existing-dataframe-in-python-pandas
#   new_weather_row.loc[i,'timestamp'] = dt

    
# write to influx
    
host='influxdb-0b85b764-1.b9873c9b.cont.dockerapp.io'
port=8086
user = 'root'
password = 'root'
dbname = 'weatherdb'
client = DataFrameClient(host, port, user, password, dbname)

print("Write DataFrame")
client.write_points(new_weather_row, 'demo')

# print("Write DataFrame with Tags")
# client.write_points(new_weather_row, 'demo', {'k1': 'v1', 'k2': 'v2'})


# how about a picture https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
# fig, axes = plt.subplots(nrows=len(mycolumns), ncols=1)
# for i, c in enumerate(new_weather_row.columns):
#    new_weather_row[c].plot(kind='bar', ax=axes[i], figsize=(12, 10), title=c)
#    plt.savefig('ah.png', bbox_inches='tight')
