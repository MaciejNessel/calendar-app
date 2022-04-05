#import Day


####        DayManager



class DayManager:
    _days = []
    _data = None

    def __init__(self, jsonManager):
        self._data = jsonManager

    #Load days that have events
    def load(self):
        self._days = self._data.loadDays

    #Add Event Id to day
    def addEventToDay(self, eventId, start, end, date = "", day = -1, month = -1, year = -1):
        pass

    #Cut string date to int array [day, month, year]
    #date format DD-MM-YYYY
    def __cutDate(self, date):
        day, month, year = date.split('-')
        
        return [day, month, year]

    #Get Day of date
    def getDay(self, date = "", day = -1, month = -1, year = -1):
        if date == "" and (day == -1 or month == -1 or year == -1):
            return None
        else:
            #todo
            pass
        pass

    #save days to JSON file
    def save(self):
        #Look for every day that have events


        pass
