import requests
import os

def download_gif(path='downloads/temp.gif'):
  response = requests.get(f"https://api.giphy.com/v1/gifs/random?api_key={os.getenv('GIPHY_API_KEY')}&tag=anime")
  uri = response.json()['data']['images']['original']['url']
  with open(path, 'wb') as f:
    f.write(requests.get(uri).content)

download_gif('./test.gif')
