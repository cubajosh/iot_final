**Temprature Project**:
It is not uncommon for people to have temperature sensors in their home. Almost everybody
has a thermostat installed in their home and almost everybody has air conditioning. However
when it comes to farming or meteorology, it becomes more complicated when getting
temperature data. When a farmer plants crops (whether it’s in a massive field or in a
greenhouse) they need complete accuracy data and the perfect temperature, humidity and light
levels to grow their desired crops. For example, you cannot just take the apple seeds from an
apple and grow it in your backyard, it will not grow, or if it does it will die very quickly. The same
goes with meteorology, while you are able to get the weather for the day on your phone, that
data comes from high tech sensors that most people cannot afford, which means weather
enthusiasts need to pay a lot of money to indulge in their hobby. Our system however, can solve
both of these problems. For the farmers, our system can detect the humidity, temperature and
the light levels to be sure that they can create the perfect environment for whatever crop they
want to grow. Our system also allows them to set a minimum and maximum level for humidity,
light and temperature. So if the temperature of the environment falls below the minimum they
have set, they will receive a warning. For the weather enthusiasts, they can receive the same
data as the farmers, however they can use it to predict the weather or to simply get the current
weather.



**Target audience**:
The target audience for this project are mostly farmers trying to set up a proper and optimal
environment for their crops. However, we realized that this system could also be used for
meteorologists trying to get accurate weather readings. This would work with both because they
both use temperature, humidity and light levels as data to either report on the weather or to
find/make a good environment for crops. This system would also be able to detect if a
thunderstorm is near because lightning is made by high humidity levels (between 60-90%) and
warm temperatures on the surface. Therefore our system would be able to detect abnormal
levels which would help meteorologists warn people about incoming storms. Our system would
also help farmers because if an environment with crops reaches a certain humidity level, the
environment will promote the growth of mold, bacteria, fungi, etc which would be incredibly
harmful for crops. So much so that an entire crop yield could be destroyed by something like
fungi growing and devouring crops. Our system would prevent this by warning the user about
high humidity levels.

**Hardware Design**
Sensors Used:
 Humidity Sensor ( dht11)
 Photoresistor

**hardware schematics**:
![image](https://user-images.githubusercontent.com/83419373/209233633-1a229252-a695-4eca-be7d-ab4f8efb46da.png)

**Mongodb Schema**:

![image](https://user-images.githubusercontent.com/83419373/209234344-b4e4a872-5675-4be4-aa68-498cb1a41541.png)


**sensor data sampling and specification**:
the humidity sesor tracks the temperature and humidity and the photoresistor tracks the light levels

Here is an example of what it looks in mongoDb:

![image](https://user-images.githubusercontent.com/83419373/209234614-8b0a7e21-ba39-4168-92b9-570ff03789cc.png)

**API Endpoints**:

GET:
ngrok:

https://81d5-66-130-174-151.ngrok.io/temps/light/1

https://81d5-66-130-174-151.ngrok.io/temps/humidity/1

https://81d5-66-130-174-151.ngrok.io/temps/1

https://81d5-66-130-174-151.ngrok.io/temps

https://81d5-66-130-174-151.ngrok.io/temps/temperatures/1

POST:
ngrok:

https://81d5-66-130-174-151.ngrok.io/temps

local:
http://127.0.0.1:5001/temps/2

POST json obj structure:
{
    "humidity": 50,
    "light levels": 100,
    "temperatures": 200
}
















