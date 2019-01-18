#retrieves weather data from Cassandra tables and renders it in Django template
from django.shortcuts import render_to_response
from django.template import RequestContext
import cPickle
import pyowm 
from cassandra.cluster import Cluster 
PYOWM_KEY = '<ENTER>'
owm = pyowm.OWM(PYOWM_KEY)

cluster = CLuster() #initiate Cassandra instance 

session = cluster.connect("weatherkeyspace") #establish Cassandra connection, using local default 

def home(request):
	if request.method == "POST":
		city = request.POST.get('city')
	else:
		city = "New York, US"

	results = session.execute('SELECT * FROM weather WHERE city = '+city+' ORDER BY time DESC LIMIT 1')


	for r in results:
		time = r[1]
		temp = r[2]
		status = r[3]
		pressure = r[4]
		humidity = r[5]
		wind = r[6]
		rain = r[7]
		clouds = r[8]

	results = session.execute('SELECT * FROM forecast WHERE city = '+city+'')

	for r in results:
		data = r[1]

	forecast_List = cPickle.loads(data.decode("hex"))

	result_dict = { 'city':city, 'time' : time, 'temp' :temp, 'status':status, 
					'pressure': pressure, 'humidity':humidity, 'wind':wind, 
					'rain': rain, 'clouds': clouds, 'forecast_list': forecast_list}

	return render_to_response('index.html', result_dict, context_instance = RequestContext(request))