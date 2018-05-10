from pyowm import OWM
import time

DOMAIN = "weather_info"

def setup(hass, config):
# def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the component."""

    API_KEY = '364b43ebe41b965c29cbea107868b6ec'
    owm = OWM(API_KEY)
    # Budapest BME Q coords ( 47.5, 19.1 )

#    add_devices([WeatherInfoSensor()])

#class WeatherInfoSensor(Entity):

#    def __init__(self):
#        self._state = None

#    @property
#    def name(self):
#        return "Weather score"

#    @property
#    def state(self):
#        return self._state

#    @property
#    def unit_of_measurement(self):
#        return ""

#    def update(self)
#        hass.sevices.call('weather_info', update)

    def handle_update(call):
        print('Sprinkle state: ' + hass.states.get('input_boolean.sprinkle_on').state)
        if hass.states.is_state('input_boolean.sprinkle_on','off') :

          min = int(call.data.get('min', 0))
          max = int(call.data.get('max', 0))

          print('Weather update in process ...')
          print('Sprinkle length min: ' + str(min) + ' min')
          print('Sprinkle length max: ' +  str(max) + ' min')

          forecaster = owm.three_hours_forecast_at_coords(47.5, 19.1)
          forecast = forecaster.get_forecast()
          weather_list = forecast.get_weathers()

          temp = 0
          humi = 0
          rain = 0
          cloud = 0

          count = 0
          for weather in weather_list:
             temp += weather.get_temperature('celsius')['temp']
             humi += weather.get_humidity()
             cloud += weather.get_clouds()
             if len( weather.get_rain() ) > 0:
                rain += weather.get_rain()['3h']
             count += 1

          temp /= count
          humi /= count
          cloud /= count
          rain *= 10 / count

          print('Weather avg temperature: ' + str(temp) + ' °C')
          print('Weather avg humidity: ' + str(humi) + ' %')
          print('Weather avg cloud coverage: ' + str(cloud) + ' %')
          print('Weather avg rain amount: ' + str(rain) + ' mm')

          score = int( (temp-15)*7.5 + (humi-50)*-0.25 + rain*-60 + (cloud-50)*-0.25 )

          print('Weather score: ' + str(score) )
          hass.services.call('input_number','set_value', { "entity_id":"input_number.weather_score", "value":int(score) })

          if score < 0:
             sprinkle_length = 0
          elif score > 100:
             sprinkle_length = max
          else:
             sprinkle_length = int(min + (max - min) * score / 100)

          print( 'Sprinkle length: ' + str(sprinkle_length) )
          hass.services.call('input_number','set_value', { "entity_id":"input_number.sprinkle_length", "value":int(sprinkle_length) })

    hass.services.register(DOMAIN, 'update', handle_update)

    # Return boolean to indicate that initialization was successfully.
    return True

