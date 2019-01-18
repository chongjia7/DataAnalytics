#retrieves weather data from DyanmoDB and renders it in Django template
from django.shortcuts import render_to_response 
from django.template import RequestContext 
import boto.dynamodb2 
from boto.dynamodb2.table import Table 
import cPickle
import pyown 

REGION ="us-east-1"

conn = boto.dynamodb2.connect_to_region(Region, aws_acess_key_id = '<enter>', aws_secret_access_key = "<enter>")
table = Table('weather', connection = conn)
forecastTable = Table('forecast', connection = conn)

PYOWM_KEY = '<ENTER>'
own = pyown.OWM(PYOWM_KEY)

def home(request):
	if request.method == "POST":
		city = request.POST.get('city')
	else:
		city = "New York, US"

	results = table.query_2(city__eq = city, reverse = True, limit = 1)
	for r in results:
		time = r["time"]
		temp = r["currentTemperature"]
		status = r['weatherStatus']
		pressure = r["pressure"]
		humidity = r["humidity"]
		wind = r["windSpeed"]
		rain = r["rainVolume"]
		clouds = r["cloudCoverage"]

	results = forecastTable.query_2(city__eq = city)

	for r in results:
		data = str(r['forecastList'])

	forecast_list = cPickle.loads(data)

	result_dict = { 'city':city, 'time' : time, 'temp' :temp, 'status':status, 
					'pressure': pressure, 'humidity':humidity, 'wind':wind, 
					'rain': rain, 'clouds': clouds, 'forecast_list': forecast_list}
	return render_to_response('index.html', result_dict, context_instance = RequestContext(request))
