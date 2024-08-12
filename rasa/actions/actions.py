# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
import requests
import os
from dotenv import load_dotenv

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

load_dotenv()

class ActionLogin(Action):

    def name(self):
        return "action_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        
        print(username, password)
        
        if not username:
            dispatcher.utter_message(text="ups, username masih kosong.")
            return []
        
        if not password:
            dispatcher.utter_message(text="ups, password masih kosong.")
            return []
        
        # API request to /login
        api_url = os.getenv("API_URL")
        url =  f"{api_url}/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            body = response.json()
            access_token = body["data"]["access_token"]
            
            url = f"{api_url}/auth/profile"
            
            response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
            if response.status_code == 200:
                body = response.json()
                name = body['data']['name']
                dispatcher.utter_message(text=f"Selamat {name}... Anda sudah berhasil masuk")
                return [SlotSet("name", body["data"]["name"]), SlotSet("username", None), SlotSet("access_token", access_token), SlotSet("password", None), SlotSet("logged_in", True)]
        
        dispatcher.utter_message(text="Maaf, anda gagal untuk masuk. Mohon dicek kembali username dan password anda")
        return [SlotSet("username", None), SlotSet("password", None), SlotSet("logged_in", False)]

class ActionCreateBook(Action):

    def name(self):
        return "action_create_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        title = tracker.get_slot("title")
        author = tracker.get_slot("author")
        summary = tracker.get_slot("summary")
        total_page = int(tracker.get_slot("total_page"))
        year = tracker.get_slot("year")
        
        api_url = os.getenv("API_URL")
        data = {
            "title": title,
            "author": author,
            "summary": summary,
            "total_page": total_page,
            "year": year
        }
        url = f"{api_url}/books"
        access_token = tracker.get_slot("access_token")
        
        response = requests.post(url, json=data, headers={"Authorization": f"Bearer {access_token}"})
        
        if response.status_code == 201:
            dispatcher.utter_message(text=f"Informasi buku berhasil ditambahkan")
        elif response.status_code == 400:
            error_message = ""
            for message in response.json()["message"]:
                error_message += f"- {message}\n"
            utter_message = f"Maaf, anda gagal untuk menambahkan buku. Terdapat kesalahan sebagai berikut: \n" + error_message
            dispatcher.utter_message(text=utter_message)
        elif response.status_code == 401:
            dispatcher.utter_message(text="Maaf, anda harus login terlebih dahulu")
        else:
            dispatcher.utter_message(text="Maaf, terdapat kesalahan dalam menambahkan buku. Silahkan coba lagi")
    
        return [SlotSet("title", None), SlotSet("author", None), SlotSet("summary", None), SlotSet("total_page", None), SlotSet("year", None)]

class ActionFindBook(Action):

    def name(self):
        return "action_find_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        title = tracker.get_slot("title")
        
        api_url = os.getenv("API_URL")
        url = f"{api_url}/books?search={title}"
        access_token = tracker.get_slot("access_token")
        
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        
        if response.status_code == 200:
            body = response.json()
            if len(body["data"]["data"]) > 0:
                book = body["data"]["data"][0]
                book_message = f"Judul: {book['title']}\nPenulis: {book['author']}\nRingkasan: {book['summary']}\nTotal Halaman: {book['total_page']}\nTahun Terbit: {book['year']}\nStatus: {book['status']}"
                dispatcher.utter_message(text=f"Informasi buku yang anda cari adalah sebagai berikut.\n" + book_message)
            else:
                dispatcher.utter_message(text="Maaf, buku yang anda cari tidak ditemukan")
        elif response.status_code == 401:
            dispatcher.utter_message(text="Maaf, anda harus login terlebih dahulu")
        else:
            dispatcher.utter_message(text="Maaf, terdapat kesalahan dalam menambahkan buku. Silahkan coba lagi")
    
        return [SlotSet("title", None)]
