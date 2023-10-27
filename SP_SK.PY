import requests
import pandas

# file_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=csv'
# response = requests.get(file_url)
# with open('celestrak_tle_data.csv', "wb") as file:
#     file.write(response.content)



dataset = pandas.read_csv("diabetes.csv")
print(dataset.head())