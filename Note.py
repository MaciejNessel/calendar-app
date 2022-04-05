

class Note:
    def __init__(self, title, text, id_):
        self.__title = title
        self.__text = text
        self.__id = id_

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text

    def get_id(self):
        return self.__id

    def set_id(self, id_):
        self.__id = id_

    def to_json(self):
        pass
        # TODO json_manager.save(this)
