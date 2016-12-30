"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.objects.objects import DefaultExit

from commands.command import ExitCommand
from utils.utils import is_none


class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """

    exit_command = ExitCommand

    def at_object_creation(self):
        self.return_exit = None

        self.db.on_success_arrive = None
        self.db.on_o_success_arrive = "has arrived."

        self.db.on_success_depart = None
        self.db.on_o_success_depart = "has departed."

        self.db.on_fail_depart = "You cannot there."
        self.db.on_o_fail_depart = None

        self.db.sync_exit = False

        self.db.is_lockable = False
        self.db.on_lock = None
        self.db.on_o_lock = None
        self.db.on_unlock = None
        self.db.on_o_unlock = None

        self.db.is_closeable = False
        self.db.on_open = None
        self.db.on_o_open = None
        self.db.on_close = None
        self.db.on_o_close = None

    # noinspection PyMethodOverriding
    def delete(self):
        if self.return_exit:
            super(Exit, self.return_exit).delete()
        super(Exit, self).delete()
        return True

    def at_traverse(self, traversing_object, destination):

        source_location = traversing_object.location
        target_location = destination # TODO is_none(destination.location, destination)

        if traversing_object.move_to(target_location):
            self.at_after_traverse(traversing_object, source_location)
        else:
            self.at_failed_traverse(traversing_object)

    @property
    def return_exit(self):
        return self.db.return_exit

    @return_exit.setter
    def return_exit(self, value):
        self.db.return_exit = value

    def sync_exit(self):
        self.db.sync_exit = True

    def unsync_exit(self):
        self.db.sync_exit = False

    def close_exit(self):
        if self.db.sync_exit:
            pass

    def open_exit(self):
        pass

    def lock_exit(self):
        pass

    def unlock_exit(self):
        pass

    def get_arrive(self):
        return self._get_message(self.db.on_success_arrive)

    def get_o_arrive(self, traversing_object, viewer):
        return self._get_o_message(
            self.db.on_o_success_arrive,
            traversing_object,
            viewer
        )

    def get_success_depart(self):
        return self._get_message(self.db.on_success_depart)

    def get_o_success_depart(self, traversing_object, viewer):
        return self._get_o_message(
            self.db.on_o_success_depart,
            traversing_object,
            viewer
        )

    def get_fail_depart(self):
        return self._get_message(self.db.on_fail_depart)

    def get_o_fail_depart(self, traversing_object, viewer):
        return self._get_o_message(
            self.db.on_on_scucces_arrive,
            traversing_object,
            viewer
        )

    @staticmethod
    def _get_message(message):
        return is_none(message)

    @staticmethod
    def _get_o_message(message, traversing_object, viewer):
        if not message:
            return None
        return "{0} {1}".format(traversing_object.get_display_name(viewer), message)

        # def at_traverse(self, traversing_object, target_location):
        #     """
        #     Override the traver se method in order to account for non-room
        #     objects. This would allow a portal into a moving entity.
        #
        #     Args:
        #         traversing_object (Object): Object traversing us.
        #         target_location (Object): The location or location's location to go
        #
        #     """
        #     target_origin = traversing_object.location
        #     target_destination = is_none(target_location.location, target_location)
        #
        #     if traversing_object.move_to(target_destination):
        #         self.announce_success_departure(traversing_object, target_origin)
        #         self.announce_arrival(traversing_object, target_destination)
        #     else:
        #         self.announce_fail_departure(traversing_object, target_origin)

        # # TODO: This is wrong should use return exist success_arrive
        # def announce_arrival(self, traversing_object, location):
        #     if not self.db.return_exit:
        #         return
        #
        #     arrival_exit = self.db.return_exit
        #     for obj in location.contents:
        #         if obj == traversing_object and arrival_exit.success_arrive:
        #             obj.msg(arrival_exit.success_arrive)
        #         elif obj != traversing_object and arrival_exit.o_success_arrive:
        #             obj.msg("{0} {1}".format(obj.get_display_name(
        #                 traversing_object), arrival_exit.o_success_arrive))
        #
        # def announce_success_departure(self, traversing_object, location):
        #     depart_exit = self
        #     for obj in location.contents:
        #         if obj == traversing_object and depart_exit.db.success_depart:
        #             obj.msg(depart_exit.db.success_depart)
        #         elif obj != traversing_object and depart_exit.db.o_success_depart:
        #             obj.msg("{0} {1}".format(traversing_object.get_display_name(
        #                 obj), depart_exit.db.o_success_depart))
        #
        # def announce_fail_departure(self, traversing_object, location):
        #     depart_exit = self
        #     for obj in location.contents:
        #         if obj == traversing_object and depart_exit.db.fail_depart:
        #             obj.msg(depart_exit.db.fail_depart)
        #         elif obj != traversing_object and depart_exit.db.o_fail_depart:
        #             obj.msg("{0} {1}".format(traversing_object.get_display_name(
        #                 obj), depart_exit.db.o_fail_depart))


class LockableExit(Exit):
    pass
