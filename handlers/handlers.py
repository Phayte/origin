class Handler(object):
    DB_HANDLER_NAME = "handler"

    def __init__(self, obj):
        self.obj = obj

        if not obj.attributes.has(self.DB_HANDLER_NAME):
            obj.attributes.add(self.DB_HANDLER_NAME, {})
        self.db_dict = obj.attributes.get(self.DB_HANDLER_NAME)

        if not self.initialized:
            self.at_handler_creation()
            self.initialized = True

    def at_handler_creation(self):
        pass

    def at_force(self):
        self.at_handler_creation()

    def __getattr__(self, item):
        if item == "obj" or item == "db_dict":
            try:
                return object.__getattribute__(self, item)
            except AttributeError:
                return None
        else:
            return self.db_dict[item] if item in self.db_dict else None

    def __setattr__(self, key, value):
        if key == "obj" or key == "db_dict":
            object.__setattr__(self, key, value)
        else:
            print("Set")
            self.db_dict[key] = value

    def __delattr__(self, item):
        if item == "obj" or item == "db_dict":
            object.__delattr__(self, item)
        else:
            del self.db_dict[item]