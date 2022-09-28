from datetime import datetime, date
from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from hospitals import Hospital


class ActionFindHospital(Action):

    def name(self) -> Text:
        return "action_find_hospital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        city = tracker.latest_message['text']
        print("location:", city)
        data = Hospital(city)
        dispatcher.utter_message(text=f"Location:{city}")
        lat = data['features'][0]['properties']['lat']
        lon = data['features'][0]['properties']['lon']
        latt = str(lat)
        print(latt)
        lonn = str(lon)
        location = latt + ',' + lonn
        url = f"https://api.foursquare.com/v3/places/search?ll={location}&radius=4000&categories=15014"
        print(url)
        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": "fsq3CWU0GcPqza3s9MjzfPgeE88/yd5DFncABcscPe7uDQY="
        }

        response = requests.get(url, headers=headers, data=payload)
        json_data = response.json()
        print(json_data)

        if json_data['results'] == []:
            dispatcher.utter_message(text="Sorry,I could not find Hospital in your location!")
        else:
            for value in json_data['results'][:3]:
                hospital_id = value['fsq_id']
                payload = "Hospital" + hospital_id
                buttons.append({'title': "{}".format(value['name']), "payload": payload})
            dispatcher.utter_button_message(text="Nearest Hospitals in your current location:", buttons=buttons)
        print(buttons)

        return []

class ActionFindAddress(Action):

    def name(self) -> Text:
        return "action_find_address"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        hos_id = tracker.latest_message['text']
        print(hos_id)
        id = (hos_id[8:32])
        print(id)
        url = f"https://api.foursquare.com/v3/places/{id}?fields=name%2Clocation"
        print(url)
        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": "fsq3CWU0GcPqza3s9MjzfPgeE88/yd5DFncABcscPe7uDQY="
        }

        response = requests.get(url, headers=headers, data=payload)
        data = response.json()
        print(data)
        name = data['name']
        add = data['location']['formatted_address']
        print(name, add)
        if data is None:
            dispatcher.utter_message(text="Sorry, I Can't Found The Address")
        else:
            dispatcher.utter_message(text="Details:\n"
                                          f"Name: {name}\n"
                                          f"Address: {add}")

        return []


class ActionFindDoctor(Action):

    def name(self) -> Text:
        return "action_Doc_details"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name = tracker.latest_message['text']
        print(name)
        if name == "Dr.M.Goki":
            dispatcher.utter_message(text=f"Name: {name}\n"
                                          f"Specialist: Cardiologist\n"
                                          f"Timing: 10.00am to 10.00pm\n"
                                          f"Contact: 9945793443")
        elif name == "Dr.G.Joyce Esther":
            dispatcher.utter_message(text=f"Name: {name}\n"
                                          f"Specialist: Neurologist\n"
                                          f"Timing: 9.30am to 6.30pm\n"
                                          f"Contact: 9946534253")
        elif name == "Dr.M.Areif Mohamed":
            dispatcher.utter_message(text=f"Name: {name}\n"
                                          f"Specialist: Paediatrician\n"
                                          f"Timing: 9.30am to 6.30pm\n"
                                          f"Contact: 8845723353")
        return []


class ActionNumber(Action):
    def name(self) -> Text:
        return "action_numbers"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message['text']

        if latest_message is None:
            dispatcher.utter_message(template="utter_ask_dob")
        else:
            born = latest_message
            print("Born :", born)
            born = datetime.strptime(born, "%d/%m/%Y").date()
            today = date.today()
            age = today.year - born.year - ((today.month,
                                             today.day) < (born.month,
                                                           born.day))
            print("Age:", age)
        return [SlotSet("age", age)]


class ActionDetails(Action):
    def name(self) -> Text:
        return "action_details"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        gender = tracker.get_slot("gender")
        dob = tracker.get_slot("dob")
        age = tracker.get_slot("age")
        number = tracker.get_slot("number")
        print(name, gender, dob, age, number)
        dispatcher.utter_message(text="Your appointment has been created successfully!")
        # dispatcher.utter_message(text="User Details:\n"
        #                               f"Name: {name}\n"
        #                               f"Gender: {gender}\n"
        #                               f"Date-of-Birth: {dob}\n"
        #                               f"Age: {age}\n"
        #                               f"Mobile.No: {number}\n")
        dispatcher.utter_message(template="utter_details", name=name, gender=gender, dob=dob, age=age, number=number)
