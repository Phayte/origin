from utils.utils import get_saver_dict


class Handler(object):
    DB_HANDLER_NAME = "handler"

    def __init__(self, obj):
        """

        :type obj: typeclasses.exits.Exit
        """
        self.obj = obj

        self.ndb = DBHandler(get_saver_dict(obj, self.DB_HANDLER_NAME, False))
        self.db = DBHandler(get_saver_dict(obj, self.DB_HANDLER_NAME))

        if not self.db.initialized:
            self.at_handler_creation()
            self.db.initialized = True

    def at_handler_creation(self):
        pass

    def at_force(self):
        self.at_handler_creation()


class DBHandler(object):
    def __init__(self, db):
        """

        :type db: dict
        """
        object.__setattr__(self, "db", db)

    def __getattr__(self, item):
        return self.db[item] if item in self.db else None

    def __setattr__(self, key, value):
        self.db[key] = value

    def __delattr__(self, item):
        del self.db[item]