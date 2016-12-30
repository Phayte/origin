from evennia.utils.create import create_object

from commands.construct import ConstructExitCmdSet
from typeclasses.objects import Object
from utils.utils import is_exit


class Construct(Object):
    def at_object_creation(self):
        super(Construct, self).at_object_creation()
        self.db.construct_modules = []
        self.db.construct_exits = []

    def at_object_receive(self, moved_obj, source_location):
        """
        If an object is not moved from the construct location, it should be
        something internal exiting the object.

        :param moved_obj:
        :param source_location:
        :return:
        """
        if not is_exit(moved_obj) and self.location != source_location:
            moved_obj.move_to(self.location)

    def at_cmdset_get(self, **kwargs):
        if "force_init" in kwargs or \
                not self.cmdset.has_cmdset("ExitCmdSet", must_be_default=True):
            self.cmdset.add_default(self.create_exit_cmdset(), permanent=False)

    def create_module(self, key):
        construct_module = create_object(
            "typeclasses.rooms.Room",
            key=key
        )

        # TODO: Need object with reference to parent

        self.db.construct_modules.append(construct_module)
        return construct_module

    def create_exit(self, key, destination):
        construct_exit = create_object(
            "typeclasses.exits.Exit",
            key=key,
            location=self,
            destination=destination
        )

        construct_return_exit = create_object(
            "typeclasses.exits.Exit",
            key=key,
            location=destination,
            destination=self
        )

        construct_exit.return_exit = construct_return_exit
        construct_return_exit.return_exit = construct_exit

        self.db.construct_exits.append(construct_exit)
        return construct_exit

    def create_exit_cmdset(self):
        return ConstructExitCmdSet(
            self.db.construct_exits,
            key='ExitCmdSet',
            format_exit_cmd_key=self.format_exit_cmd_key
        )

    def delete(self):
        for construct_exit in self.db.construct_exits:
            if construct_exit:
                construct_exit.delete()

        for construct_module in self.db.construct_modules:
            if construct_module:
                construct_module.delete()

        super(Construct, self).delete()
        return True

    def format_exit_cmd_key(self, exit_obj):
        return "{0}-{1}".format(self.id, exit_obj.db_key.strip().lower())
