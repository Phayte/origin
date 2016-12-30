#from handlers.handlers import Handler
from evennia.utils.search import object_search

from utils.utils import is_none


class Handler(object):
    DB_HANDLER_NAME = "handler"

    def __init__(self, obj):
        self.obj = obj

        if not obj.attributes.has(self.DB_HANDLER_NAME):
            obj.attributes.add(self.DB_HANDLER_NAME, {})
        self.db_dict = obj.attributes.get(self.DB_HANDLER_NAME)

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


class ExitRoleplayHandler(Handler):
    DB_HANDLER_NAME = "exit_rp_handler"

    def __init__(self, exit_obj):
        super(ExitRoleplayHandler, self).__init__(exit_obj)
        # TODO: set to none later
        self.on_success_arrive = "You have arrived."
        self.on_o_success_arrive = "has arrived."

        # TODO: set to none later
        self.on_success_depart = "You have departed."
        self.on_o_success_depart = "has departed."

        self.on_fail_depart = "You cannot go there."
        # TODO: set to none later
        self.on_o_fail_depart = "fails to leave."

    def get_arrive(self):
        arrive_exit = is_none(self.return_exit, self)
        # noinspection PyProtectedMember
        return arrive_exit._get_message(arrive_exit.on_success_arrive)

    def get_o_arrive(self, traversing_object, viewer):
        return self._get_o_message(
            self.on_o_success_arrive,
            traversing_object,
            viewer
        )

    def get_success_depart(self):
        return self._get_message(self.on_success_depart)

    def get_o_success_depart(self, traversing_object, viewer):
        return self._get_o_message(
            self.on_o_success_depart,
            traversing_object,
            viewer
        )

    def get_fail_depart(self):
        return self._get_message(self.on_fail_depart)

    def get_o_fail_depart(self, traversing_object, viewer):
        return self._get_o_message(
            self.on_o_success_arrive,
            traversing_object,
            viewer
        )

    @staticmethod
    def _get_message(message):
        return message

    @staticmethod
    def _get_o_message(message, traversing_object, viewer):
        if not message:
            return None
        return "{0} {1}".format(traversing_object.get_display_name(viewer),
                                message)
#
# # class ExitAccessHandler(Handler):
# #     DB_HANDLER_NAME = "exit_access_handler"
# #
# #     def __init__(self, exit_obj):
# #         super(ExitAccessHandler, self).__init__(exit_obj)
#
#
#
