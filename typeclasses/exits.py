"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.objects.objects import DefaultExit
from evennia.utils import lazy_property

from commands.command import ExitCommand
from handlers.exits import ExitRoleplayHandler


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
        """
        Departs will always be used since that is the exit tied with where players were last
        at. However, the arrival message will need to be deteremined by if return_exit exists.

        :return:
        """
        self.return_exit = None

        # # region Movement Descriptors
        # self.db.on_success_arrive = None
        # self.db.on_o_success_arrive = "has arrived."
        #
        # self.db.on_success_depart = None
        # self.db.on_o_success_depart = "has departed."
        #
        # self.db.on_fail_depart = "You cannot there."
        # self.db.on_o_fail_depart = None
        # # endregion

    def at_traverse(self, traversing_object, destination):

        source_location = traversing_object.location
        target_location = destination

        if traversing_object.move_to(target_location):
            self.at_after_traverse(traversing_object, source_location)
        else:
            self.at_failed_traverse(traversing_object)

    def at_failed_traverse(self, traversing_object):
        exit_obj = traversing_object.ndb.last_exit
        location = traversing_object.location

        if exit_obj:
            for obj in location.contents:
                if obj == self:
                    obj.msg(exit_obj.rp.get_success_depart())
                else:
                    obj.msg(exit_obj.rp.get_o_success_depart(self, obj))

            del traversing_object.ndb.last_exit
        else:
            traversing_object.msg("You cannot go there.")

    # noinspection PyMethodOverriding
    def delete(self):
        if self.return_exit:
            super(Exit, self.return_exit).delete()
        super(Exit, self).delete()
        return True

    # region Properties
    @property
    def return_exit(self):
        return self.db.return_exit

    @return_exit.setter
    def return_exit(self, value):
        self.db.return_exit = value

    @return_exit.deleter
    def return_exit(self):
        del self.db.return_exit

    # @lazy_property
    # def access(self):
    #     pass
    #     #return ExitAccessHandler(self)
    #
    @lazy_property
    def rp(self):
        return ExitRoleplayHandler(self)
    # endregion

    # def get_arrive(self):
    #     arrive_exit = is_none(self.return_exit, self)
    #     # noinspection PyProtectedMember
    #     return arrive_exit._get_message(arrive_exit.db.on_success_arrive)
    #
    # def get_o_arrive(self, traversing_object, viewer):
    #     return self._get_o_message(
    #         self.db.on_o_success_arrive,
    #         traversing_object,
    #         viewer
    #     )
    #
    # def get_success_depart(self):
    #     return self._get_message(self.db.on_success_depart)
    #
    # def get_o_success_depart(self, traversing_object, viewer):
    #     return self._get_o_message(
    #         self.db.on_o_success_depart,
    #         traversing_object,
    #         viewer
    #     )
    #
    # def get_fail_depart(self):
    #     return self._get_message(self.db.on_fail_depart)
    #
    # def get_o_fail_depart(self, traversing_object, viewer):
    #     return self._get_o_message(
    #         self.db.on_on_scucces_arrive,
    #         traversing_object,
    #         viewer
    #     )

    @staticmethod
    def format_exit_key(exit_obj):
        return exit_obj.db_key.strip().lower()

    # @staticmethod
    # def _get_message(message):
    #     return message
    #
    # @staticmethod
    # def _get_o_message(message, traversing_object, viewer):
    #     if not message:
    #         return None
    #     return "{0} {1}".format(traversing_object.get_display_name(viewer),
    #                             message)

    pass
