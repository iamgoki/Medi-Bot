import requests


def Hospital(city):
    api_address = f'https://api.geoapify.com/v1/geocode/search?text={city}&apiKey=258e57f1ab3b401eba7fcc46de414de6'
    url = api_address
    json_data = requests.get(url).json()
    print(json_data)
    return json_data








