import requests
from django.shortcuts import render,redirect
from .models import City
# Create your views here.

def index(request):
    message=''
    err_message=''
    messageShow=''
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7cec8a16a014b57f940965c646643c1a'
    if request.method=="POST":
        cityName=request.POST.get('cityName')
        cityN=City(name=cityName)
        city1=cityName
        countCity=City.objects.filter(name=city1).count()
        if countCity==0:
            r=requests.get(url.format(cityName)).json()
            print(r)
            if r['cod']==200:
                cityN.save()
            #elif city1==' ':
                #err_message=''
                 
            else:
                err_message='City Does Not Exist in the World'
        else:
            err_message='City already exists'
        if err_message:
           message=err_message
           messageShow='is-danger'
        else:
           message='City Added!'
           messageShow='is-success'

            
    weather_data=[]
    cities=City.objects.all()
    for city in cities:
        r=requests.get(url.format(city.name)).json()
        weather_city={'city':city.name,'temp':r['main']['temp'],'desc':r['weather'][0]['description'],'icon':r['weather'][0]['icon'],}
        weather_data.append(weather_city)
    weather_datas={'weather_data':weather_data,'message':message,'messageShow':messageShow}
    print(weather_datas)
    return render(request,'weather/weather.html',weather_datas)


def delete(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')