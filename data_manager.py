import os
import requests
from requests.auth import HTTPBasicAuth

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_endpoint = "https://api.sheety.co/1d0173a84f9c74a0fa3545b9f8928031/flightDeals/prices"
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.users_endpoint = os.environ["SHEETY_USERS_ENDPOINT"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.sheet_data = {}
        self.customer_data = {}

    def get_sheet_data(self):
        headers = {
            "Authorization": os.environ["SHEETY_AUTHORIZATION"]
        }
        response = requests.get(url=self.sheety_endpoint, headers=headers)
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def put_sheet_data(self):
        headers = {
            "Authorization": os.environ["SHEETY_AUTHORIZATION"]
        }
        for city in self.sheet_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{self.sheety_endpoint}/{city['id']}", json=new_data, headers=headers)
            print(response.text)


    def get_customer_email(self):
        response = requests.get(url=self.users_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data