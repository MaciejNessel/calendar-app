from App.Days.Day import Day
import json

class DayManager:
    def __init__(self, json_manager):
        self.__days = {}
        self.__json_manager = json_manager

    # Load days that have events
    def load(self):
        self.__days.clear()
        data = self.__json_manager.get_data_per_days()
        for day in data:
            new_day = Day(day.get('date'), day.get('events'), day.get('notes'))
            self.__days.update({day.get('date'): new_day})

    # Add Event Id to day
    def add_event_to_day(self, event_id, start, end, date="", day=-1, month=-1, year=-1):
        event_info = {
                "id_" : event_id,
                "start": start,
                "end": end
            }

        if self.get_day(date=date) == None:
            new_day = Day(date, events_=[], notes=[])
            new_day.add_event_to_day(event=event_info)
            self.__days.update({date: new_day})
        else:
            old_day = self.get_day(date=date)
            old_day.add_event_to_day(event_info)

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
        elif date == "":
            day_ = ""
            month_ = ""
            year_ = ""
            if day < 10:
                day_ = "0"
            day_ += str(day)
            if month < 10:
                month_ = "0"
            month_ += str(month)
            key = str(year) + "-" + month_ + "-" + day_
            return self.__days.get(key)
        else:
            return self.__days.get(date)

    def delete_event(self, event_id):
        to_remove = []
        for x in self.__days.keys():
            if self.__days[x].delete_event(event_id):
                to_remove.append(x)

        for x in to_remove:
            self.__days.pop(x)

    # save days to JSON file
    def save(self):
        result = {"dataPerDay": []}
        for day in self.__days.items():
            result["dataPerDay"].append((json.loads(day[1].to_json())))
        return result
