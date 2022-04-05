


####        Event

class Event:
    _title = ""
    _shortDesc = ""
    _desc = ""
    _id = -1
    _noteId = -1
    
    def __init__(self, title, shortDesc, desc, id, noteId):
        self._title = title
        self._shortDesc = shortDesc
        self._desc = desc
        self._id = id
        self._notesId = []

    #Return Event object in Json format
    def toJSON(self):
        return []

    #Getters to all Atributes

    def getTitle(self):
        return self._title

    def getShortDesc(self):
        return self._shortDesc

    def getDesc(self):
        return self._desc

    def getId(self):
        return self._id

    def getNotesId(self):
        return self._notesId

    #Setter to _title

    def setTitle(self, title):
        self._title = title

    #Setter to _shortDesc

    def setShortDesc(self, shortDesc):
        self._shortDesc = shortDesc
    
    #Setter to _desc

    def setDesc(self, desc):
        self._desc = desc

    #Add note of Id to _notesId(Event)

    def addNote(self, noteId):
        self._notesId.append(noteId)

    #Remove note of Id from _notesId(Event)

    def removeNote(self, noteId):
        self._notesId.remove(noteId)