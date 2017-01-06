from evennia.utils.create import create_object

from commands.construct import ConstructExitCmdSet
from typeclasses.exits import Exit
from typeclasses.objects import Object
from utils.utils import is_exit


class Construct(Object):
    def at_object_creation(self):
        super(Construct, self).at_object_creation()
        self.db.modules = []
        self.db.exits = []

    def at_object_receive(self, moved_obj, source_location):
        """
        If an object is not moved from the construct location, it should be
        something internal exiting the object.

        :param moved_obj:
        :param source_location:
        :return:
        """
        if not is_exit(moved_obj) and self.location != source_location:
            moved_obj.move_to(self.location, quiet=True, move_hooks=False)

    def at_cmdset_get(self, **kwargs):
        if "force_init" in kwargs or \
                not self.cmdset.has_cmdset("ExitCmdSet", must_be_default=True):
            self.cmdset.add_default(self.create_exit_cmdset(), permanent=False)

    # region Properties
    def default_exit_get(self):
        return self.db.default_exit

    def default_exit_set(self, value):
        self.db.default_exit = value

    def default_exit_del(self):
        del self.db.default_exit

    default_exit = property(default_exit_get,
                            default_exit_set,
                            default_exit_del)
    # endregion

    def create_module(self, key):
        construct_module = create_object(
            "typeclasses.rooms.Room",
            key=key
        )

        # TODO: Need object with reference to parent

        self.db.modules.append(construct_module)
        return construct_module

    def create_exit(self, key, destination, aliases=None):
        construct_exit = Exit.create_exit(
            key,
            self,
            destination,
            aliases
        )

        construct_exit.link.pair_return_exit()
        self.db.exits.append(construct_exit)
        if len(self.db.exits) == 1:
            self.default_exit = construct_exit

        return construct_exit

    def create_exit_cmdset(self):
        return ConstructExitCmdSet(
            self.db.exits,
            key='ExitCmdSet',
            format_exit_name=self.format_exit_name
        )

    def delete(self):
        for construct_exit in self.db.exits:
            if construct_exit:
                construct_exit.delete()

        for construct_module in self.db.modules:
            if construct_module:
                construct_module.delete()

        super(Construct, self).delete()
        return True

    def format_exit_name(self, exit_name):
        return "{0}-{1}".format(self.id, exit_name.strip().lower())
