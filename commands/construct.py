from evennia.commands.cmdset import CmdSet
from evennia.commands.default.building import ObjManipCommand
from evennia.utils.create import create_object

from commands.command import Command, ExitCommand
from typeclasses.exits import Exit


class ConstructExitCmdSet(CmdSet):
    exit_priority = Exit.priority

    def __init__(self, exit_objs, cmdsetobj=None, key=None,
                 format_exit_cmd_key=None):
        super(ConstructExitCmdSet, self).__init__(cmdsetobj, key)

        self.key = key
        self.priority = self.exit_priority
        self.duplicates = True

        if not format_exit_cmd_key:
            format_exit_cmd_key = self._format_exit_cmd_key

        for exit_obj in exit_objs:
            cmd = ExitCommand(key=format_exit_cmd_key(exit_obj),
                              # TODO Need to fix aliases
                              aliases=exit_obj.aliases.all(),
                              locks=str(exit_obj.locks),
                              auto_help=False,
                              destination=exit_obj.db_destination,
                              arg_regex=r"^$",
                              is_exit=True,
                              obj=exit_obj,
                              help_category="Exits")
            self.add(cmd)

    @staticmethod
    def _format_exit_cmd_key(exit_obj):
        return exit_obj.db_key.strip().lower()


class CmdConstruct(Command):
    key = "construct"
    help_category = "Construct"

    def func(self):
        construct = create_object(
            "typeclasses.construct.Construct",
            key="Ship",
            location=self.caller.location
        )
        self.caller.msg("Created construct #{0}".format(construct.id))

        construct_module = construct.create_module("Airlock Room")
        self.caller.msg("Created module #{0}".format(construct_module.id))

        construct_exit = construct.create_exit("Airlock Exit",
                                               construct_module)
        self.caller.msg("Created exit #{0}".format(construct_exit.id))


class CmdBoard(ObjManipCommand):
    key = "board"
    help_category = "Construct"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: board ship[/entrance]")
            return

        construct_name = self.lhs_objattr[0]['name']
        exit_name = self.lhs_objattr[0]['attrs']

        if len(exit_name) > 1:
            caller.msg("You can only specify one entrance.")

        construct = self.caller.search(construct_name)
        if not construct:
            return

        construct_exit = self.caller.search(exit_name[0], location=construct)
        if not construct_exit:
            return

        caller.execute_cmd(construct.format_exit_cmd_key(construct_exit))


class CmdSetConstruct(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdConstruct)
