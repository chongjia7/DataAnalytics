#retrieves weather data from MongoDB and renders it in Django template
from django.shortcuts import render_to_response
from django.template import RequestContext
#import cPickle
import pyowm 
from pymongo import MongoClient

client = MongoClient('mongodb://root:password@hostname:53688/weather')
db = client['weather']
weather_collection = db['current']
forecast_collection = db['forecast']

PYOWM_KEY = '<ENTER>'
owm = pyowm.OWM(PYOWM_KEY)

def home(request):
	if request.method == "POST":
		city = request.POST.get('city')
	else:
		city = "New York, US"

	results = weather_collection.find({"city": city}).sort("_id", -1).limit(1)

	for r in results:
		time = r["time"]
		temp = r["currentTemperature"]
		status = r['weatherStatus']
		pressure = r["pressure"]
		humidity = r["humidity"]
		wind = r["windSpeed"]
		rain = r["rainVolume"]
		clouds = r["cloudCoverage"]

	results = forecast_collection.find({"city": city})

	for r in results:
		data = str(r['forecastList'])

	forecast_list = data

	result_dict = { 'city':city, 'time' : time, 'temp' :temp, 'status':status, 
					'pressure': pressure, 'humidity':humidity, 'wind':wind, 
					'rain': rain, 'clouds': clouds, 'forecast_list': forecast_list}
					
	return render_to_response('index.html', result_dict, context_instance = RequestContext(request))