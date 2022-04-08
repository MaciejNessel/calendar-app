from App.Days.Day import Day
import json

class DayManager:
    def __init__(self, json_manager):
        self.__days = {}
        self.__json_manager = json_manager

    # Load days that have events
    def load(self):
        data = self.__json_manager.get_data_per_days()
        for day in data:
            new_day = Day(day.get('date'), day.get('events'), day.get('notes'))
            self.__days.update({day.get('date'): new_day})

    # Add Event Id to day
    def add_event_to_day(self, event_id, start, end, date="", day=-1, month=-1, year=-1):
        pass

    # Cut string date to int array [day, month, year]
    # date format DD-MM-YYYY
    @staticmethod
    def __cut_date(date):
        day, month, year = date.split('-')
        return [day, month, year]

    # Get Day of date
    def get_day(self, date="", day=-1, month=-1, year=-1):
        if date == "" and (day == -1 or month == -1 or year == -1):
            return None
        else:
            # todo
            pass
        pass

    # save days to JSON file
    def save(self):
        result = {"dataPerDay": []}
        for day in self.__days.items():
            result["dataPerDay"].append((json.loads(day[1].to_json())))
        return result
