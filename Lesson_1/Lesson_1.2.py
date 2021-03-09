import requests

from pprint import pprint
import urllib


link = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz'

#key = 'P0ndPwROMw3PjKkJBMOxkSCUHU4oxFcr279hC1WP'
params = {'api_key': 'P0ndPwROMw3PjKkJBMOxkSCUHU4oxFcr279hC1WP'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',

}

response = requests.get(link, params=params, headers=headers)

j_body = response.json()
pprint(j_body.get('photos')[0].get('img_src'))

photo_link = j_body.get('photos')[0].get('img_src')


urllib.request.urlretrieve(photo_link, 'my_image.jpg')