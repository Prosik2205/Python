import requests

def get_and_filter_data(api_url, filter_params):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        filtered_data = [item for item in data if all(item.get(key) == value for key, value in filter_params.items())]

        return filtered_data
    else:
        print(f"Помилка при запиті: {response.status_code}")
        return None

api_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=json" 
filter_params = {"OBJECT_NAME": "PSYCHE"}

filtered_data = get_and_filter_data(api_url, filter_params)


print(filtered_data)
 
