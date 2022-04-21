import json
import uuid
from shutil import copyfile


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
            users_file = open("../../users/users_list.json")
            users_list = json.load(users_file)
            users_file.close()
            return users_list['users']
        except FileNotFoundError:
            print("File users_list.json doesn't exist!")
            json_object = json.dumps({"users": []})
            with open("../../users/users_list.json", "w") as outfile:
                outfile.write(json_object)
            return []

    def load_data(self, username):
        try:
            user_file = open("../../users/" + username + ".json")
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

        copyfile('../../users/' + self.__username + '.json', '../../users/old/' + self.__username + '.json')

        with open('../../users/' + self.__username + '.json', 'w') as f:
            json.dump(result, f, indent=2)

    @staticmethod
    def create_new_user(username):
        try:
            users_file = open("../../users/users_list.json")
            users_json = json.load(users_file)
        except FileNotFoundError:
            users_json = json.dumps({"users": []})

        for user in users_json.get('users'):
            if user.get('username') == username:
                return [False, "User: " + username + " exist."]

        users_json.get('users').append({
            "username": username
        })
        copyfile('../../users/users_list.json', '../../users/old/users_list.json')
        with open('../../users/users_list.json', 'w') as f:
            json.dump(users_json, f, indent=2)

        users_data = {
            "username": username,
            "eventDetails": [],
            "noteDetails": [],
            "dataPerDay": []
        }
        with open('../../users/' + username + '.json', 'w') as f:
            json.dump(users_data, f, indent=2)

        return [True, 'User added successfully.']