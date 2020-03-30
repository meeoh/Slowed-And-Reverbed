import requests


def download_gif(path='downloads/'):
  response = requests.get('https://api.giphy.com/v1/gifs/random?api_key=oYxKvFCQ3G0Upud5W1LXXIt3JuIV1sUt&tag=anime')
  uri = response.json()['data']['image_url']
  with open(path, 'wb') as f:
    f.write(requests.get(uri).content)
