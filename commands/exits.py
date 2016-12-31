from evennia.commands.default.building import ObjManipCommand
from utils.utils import is_construct, is_exit


class CmdOpenCloseExit(ObjManipCommand):
    key = "open"
    aliases = ["close"]
    locks = "cmd:all()"
    help_category = "Exits"

    def func(self):
        caller = self.caller
        if not self.args:
            self.caller.msg("Usage: open|close [construct/]exit")
            return

        arg1 = self.lhs_objattr[0]['name']
        arg2 = self.lhs_objattr[0]['attrs']

        exit_location = None
        if len(arg2) > 1:
            caller.msg("You can only specify one exit.")
        elif len(arg2) == 1:
            construct = caller.search(arg1)
            if not construct:
                return
            if not is_construct(construct):
                self.caller.msg("That is not a valid construct.")
                return

            exit_location = construct
            arg1 = arg2[0]
        else:
            exit_location = self.caller.location

        exit_obj = self.caller.search(arg1, location=exit_location)
        if not exit_obj:
            return
        if not is_exit(exit_obj):
            self.caller.msg("That is not a valid exit.")
            return

        if self.cmdstring == "open":
            exit_obj.control.open(caller)
        elif self.cmdstring == "close":
            exit_obj.control.close(caller)
