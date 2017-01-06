from evennia.commands.cmdset import CmdSet
from evennia.commands.default.building import ObjManipCommand
from evennia.utils.create import create_object

from commands.command import Command, ExitCommand
from typeclasses.exits import Exit
from utils.utils import is_exit, is_construct


class ConstructExitCmdSet(CmdSet):
    exit_priority = Exit.priority

    def __init__(self, exit_objs, cmdset_obj=None, key=None,
                 format_exit_name=None):
        super(ConstructExitCmdSet, self).__init__(cmdset_obj, key)

        self.key = key
        self.priority = self.exit_priority
        self.duplicates = True

        if not format_exit_name:
            format_exit_name = self._format_exit_name

        for exit_obj in exit_objs:
            key = format_exit_name(exit_obj.key)
            aliases = \
                [format_exit_name(alias) for alias in exit_obj.aliases.all()]

            cmd = ExitCommand(key=key,
                              aliases=aliases,
                              locks=str(exit_obj.locks),
                              auto_help=False,
                              destination=exit_obj.db_destination,
                              arg_regex=r"^$",
                              is_exit=True,
                              obj=exit_obj,
                              help_category="Exits")
            self.add(cmd)

    @staticmethod
    def _format_exit_name(exit_name):
        return exit_name.strip().lower()


class CmdConstruct(Command):
    key = "construct"
    help_category = "Construct"

    def func(self):
        # noinspection PyUnresolvedReferences
        caller = self.caller
        construct = create_object(
            "typeclasses.construct.Construct",
            key="Ship",
            location=caller.location
        )
        caller.msg("Created construct #{0}".format(construct.id))

        construct_module = construct.create_module("Airlock Room")
        caller.msg("Created module #{0}".format(construct_module.id))

        construct_exit = construct.create_exit("Airlock Exit",
                                               construct_module,
                                               ['al'])
        caller.msg("Created exit #{0}".format(construct_exit.id))


class CmdBoard(ObjManipCommand):
    key = "board"
    help_category = "Construct"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: board construct[/exit]")
            return

        construct_name = self.lhs_objattr[0]['name']
        exit_name = self.lhs_objattr[0]['attrs']

        if len(exit_name) > 1:
            caller.msg("You can only specify one exit.")

        construct = caller.search(construct_name)
        if not construct:
            return
        if not is_construct(construct):
            caller.msg("That is not a valid construct.")
            return

        if len(exit_name) == 1:
            construct_exit = caller.search(exit_name[0], location=construct)
            if not construct_exit:
                return
            if not is_exit(construct_exit):
                caller.msg("That is not a valid exit.")
                return
        else:
            construct_exit = construct.default_exit
            if not construct_exit:
                caller.msg("There is no exit for the construct")
                return

        caller.execute_cmd(construct.format_exit_name(construct_exit.key))


class CmdSetConstruct(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdConstruct)
