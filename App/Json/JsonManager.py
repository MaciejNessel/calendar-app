import json
import uuid
from shutil import copyfile

import requests
from kivy.factory import Factory

FILES_DIR = '../../'


class JsonManager:
    def __init__(self):
        self.__event_details = None
        self.__note_details = None
        self.__data_per_day = None
        self.__username = None

    @staticmethod
    def generate_id():
        return uuid.uuid1()

    @staticmethod
    def get_users():
        try:
            users_file = open(FILES_DIR + "users/users_list.json")
            users_list = json.load(users_file)
            users_file.close()
            return users_list['users']
        except FileNotFoundError:
            print("File users_list.json doesn't exist!")
            json_object = json.dumps({"users": []})
            with open(FILES_DIR + "users/users_list.json", "w") as outfile:
                outfile.write(json_object)
            return []

    def load_data(self, username):
        try:
            user_file = open(FILES_DIR + "users/" + username + ".json")
            user = json.load(user_file)
            user_file.close()
            self.__event_details = user['eventDetails']
            self.__note_details = user['noteDetails']
            self.__data_per_day = user['dataPerDay']
            self.__username = username
            return True
        except FileNotFoundError:
            print("User:", username, "doesn't exist!")
            return False
        except KeyError:
            print("Bad user", username, " data file structure!")
            return False

    def get_data_per_days(self):
        return self.__data_per_day

    def get_events(self):
        return self.__event_details

    def get_notes(self):
        return self.__note_details

    def save(self, note_manager, event_manager, day_manager):
        result = {}
        user = {'username': self.__username}
        result.update(user)
        evens_json = event_manager.save()
        result.update(evens_json)
        notes_json = note_manager.save()
        result.update(notes_json)
        days_json = day_manager.save()
        result.update(days_json)

        copyfile(FILES_DIR + 'users/' + self.__username + '.json', FILES_DIR + 'users/old/' + self.__username + '.json')

        with open(FILES_DIR + 'users/' + self.__username + '.json', 'w') as f:
            json.dump(result, f, indent=2)

    @staticmethod
    def create_new_user(username):
        try:
            users_file = open(FILES_DIR + "users/users_list.json")
            users_json = json.load(users_file)
        except FileNotFoundError:
            users_json = json.dumps({"users": []})

        for user in users_json.get('users'):
            if user.get('username') == username:
                return [False, "User: " + username + " exist."]

        users_json.get('users').append({
            "username": username
        })
        copyfile(FILES_DIR + 'users/users_list.json', FILES_DIR + 'users/old/users_list.json')
        with open(FILES_DIR + 'users/users_list.json', 'w') as f:
            json.dump(users_json, f, indent=2)

        users_data = {
            "username": username,
            "eventDetails": [],
            "noteDetails": [],
            "dataPerDay": []
        }
        with open(FILES_DIR + 'users/' + username + '.json', 'w') as f:
            json.dump(users_data, f, indent=2)

        return [True, 'User added successfully.']

    @staticmethod
    def get_json_from_file(filepath, error=""):
        try:
            file = open(filepath, "r")
            result = json.load(file)
            file.close()
            return result
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print(error)
            return None

    # TODO obslugę dodawania użytkowników o tej samej nazwie - aktualnie dane są nadpisywane!
    # Przywracanie danych: https://jsonblob.com/api/jsonBlob/967425735073742848
    @staticmethod
    def get_data_from_url(url):
        r = None
        try:
            r = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.ConnectionError):
            print("Wrong url")
            return

        try:
            r = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print("Request wrong format.")

        if not r.get("users_list") or not r.get("user_data"):
            return

        return r

    @staticmethod
    def import_data(url):
        r = JsonManager.get_data_from_url(url)
        if not r:
            return False

        users_list = JsonManager.get_json_from_file(FILES_DIR + "users/users_list.json")
        if not users_list:
            users_file = open(FILES_DIR + "users/users_list.json", "w")
            users_list = {"users": []}

        for user in r.get("users_list", {}):
            users_list.get('users').append(user)

        with open(FILES_DIR + "/users/users_list.json", 'w') as f:
            json.dump(users_list, f, indent=2)

        for user in r.get("user_data", {}):
            username = user.get('username')
            with open(FILES_DIR + "/users/" + username + ".json", 'w') as f:
                json.dump(user, f, indent=2)

        return True

    @staticmethod
    def prepare_data_to_export():
        users_list = JsonManager.get_json_from_file(filepath=FILES_DIR+"/users/users_list.json",
                                                    error="Reading file users_list.json failed.")
        if not users_list:
            return False

        users_data_to_export = {
            "users_list": [],
            "user_data": []
        }

        for users in users_list.get('users'):
            username = users.get('username')
            user_json = JsonManager.get_json_from_file(filepath=FILES_DIR + "/users/" + username + ".json")
            if not user_json:
                continue
            users_data_to_export.get('users_list').append({"username": username})
            users_data_to_export.get('user_data').append(user_json)

        return users_data_to_export

    @staticmethod
    def export_data():
        users_data_to_export = JsonManager.prepare_data_to_export()
        url = None
        if users_data_to_export:
            r = requests.post('https://jsonblob.com/api/jsonBlob',
                              data=json.dumps(users_data_to_export),
                              headers={"Content-Type": "application/json", "Accept": "application/json"})
            url = r.headers.get('Location')
        return url
