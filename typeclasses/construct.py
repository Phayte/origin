from evennia.commands.cmdset import CmdSet
from evennia.utils.create import create_object

from commands.command import ExitCommand
from typeclasses.exits import Exit
from typeclasses.objects import Object


class Construct(Object):
    def at_object_creation(self):
        super(Construct, self).at_object_creation()
        self.db.construct_modules = []
        self.db.construct_exits = []

    def at_object_receive(self, moved_obj, source_location):
        if not self.is_exit(moved_obj):
            moved_obj.move_to(self.location)

    def at_cmdset_get(self, **kwargs):
        if "force_init" in kwargs or not self.cmdset.has_cmdset("ExitCmdSet", must_be_default=True):
            self.cmdset.add_default(self.create_exit_cmdset(), permanent=False)
            # for construct_exit in self.db.construct_exits:
            #     self.cmdset.add_default(construct_exit.create_exit_cmdset(construct_exit), permanent=False)

    def create_module(self, key):
        construct_module = create_object(
            "typeclasses.rooms.Room",
            key=key
        )

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
        exit_cmdset = CmdSet(None)
        exit_cmdset.key = 'ExitCmdSet'
        exit_cmdset.priority = Exit.priority
        exit_cmdset.duplicates = True

        for exit_obj in self.db.construct_exits:
            # create an exit command. We give the properties here,
            # to always trigger metaclass preparations
            cmd = ExitCommand(key=self.get_exit_command_key(exit_obj.db_key.strip().lower()),
                              aliases=exit_obj.aliases.all(),
                              locks=str(exit_obj.locks),
                              auto_help=False,
                              destination=exit_obj.db_destination,
                              arg_regex=r"^$",
                              is_exit=True,
                              obj=exit_obj,
                              help_category="Exits")
            # TODO: maybe delete help category later
            exit_cmdset.add(cmd)

        return exit_cmdset

    def delete(self):
        for construct_exit in self.db.construct_exits:
            if construct_exit:
                construct_exit.delete()

        for construct_module in self.db.construct_modules:
            if construct_module:
                construct_module.delete()

        super(Construct, self).delete()
        return True

    def is_exit(self, obj):
        return obj.destination

    def get_exit_command_key(self, exit_name):
        return "{0} {1}".format(self.id, exit_name)
