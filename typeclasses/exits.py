"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.objects.objects import DefaultExit
from evennia.utils import lazy_property

from commands.command import ExitCommand
from handlers.exits import ExitBaseHandler, ExitControlHandler


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
                if obj == traversing_object:
                    obj.msg(exit_obj.rp.get_fail_depart())
                else:
                    obj.msg(exit_obj.rp.get_o_fail_depart(self, obj))

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
    def return_exit_get(self):
        return self.db.return_exit

    def return_exit_set(self, value):
        self.db.return_exit = value

    def return_exit_del(self):
        del self.db.return_exit

    return_exit = property(return_exit_get, return_exit_set, return_exit_del)

    @lazy_property
    def control(self):
        return ExitControlHandler(self)

    @lazy_property
    def rp(self):
        return ExitBaseHandler(self)

    # endregion

    @staticmethod
    def format_exit_key(exit_obj):
        return exit_obj.db_key.strip().lower()

    pass
