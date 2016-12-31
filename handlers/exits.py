from .handlers import Handler

from utils.utils import is_none


class ExitRoleplayHandler(Handler):
    DB_HANDLER_NAME = "exit_rp_handler"

    def __init__(self, exit_obj):
        super(ExitRoleplayHandler, self).__init__(exit_obj)

    # noinspection PyAttributeOutsideInit
    def at_handler_creation(self):
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
            self.on_o_fail_depart,
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


class ExitAccessHandler(Handler):
    DB_HANDLER_NAME = "exit_access_handler"

    def __init__(self, exit_obj):
        super(ExitAccessHandler, self).__init__(exit_obj)
