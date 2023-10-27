import requests

file_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=tle'
response = requests.get(file_url)
with open('celestrak_tle_data.txt', "wb") as file:
    file.write(response.content)