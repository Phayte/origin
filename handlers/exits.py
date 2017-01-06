from .handlers import Handler

from utils.utils import is_none
from utils import bits


class ExitLinkHandler(Handler):
    DB_HANDLER_NAME = "exit_link_handler"

    def __init__(self, exit_obj):
        super(ExitLinkHandler, self).__init__(exit_obj)

    def return_exit_get(self):
        return self.db.return_exit

    def return_exit_set(self, value):
        self.db.return_exit = value

    def return_exit_del(self):
        del self.db.return_exit

    return_exit = property(return_exit_get,
                           return_exit_set,
                           return_exit_del)

    def pair_return_exit(self, key=None, aliases=None, copy_aliases=True):
        key = is_none(key, self.obj.key)
        if not aliases and copy_aliases:
            aliases = self.obj.aliases.all()

        if not self.return_exit:
            self.return_exit = self.obj.create_exit(
                key,
                self.obj.destination,
                self.obj.location,
                aliases
            )

        self.return_exit.link.return_exit = self.obj

        return self.return_exit



class ExitMessageHandler(Handler):
    DB_HANDLER_NAME = "exit_rp_handler"

    def __init__(self, exit_obj):
        super(ExitMessageHandler, self).__init__(exit_obj)

        # TODO: Delete
        del self.db.initialized

    # noinspection PyAttributeOutsideInit
    def at_handler_creation(self):
        # TODO: maybe just delete these all later?
        # TODO: set to none later
        self.db.on_success_arrive = "You have arrived."
        self.db.on_o_success_arrive = "has arrived."

        # TODO: set to none later
        self.db.on_success_depart = "You have departed."
        self.db.on_o_success_depart = "has departed."

        self.db.on_fail_depart = "You fail to depart."
        # TODO: set to none later
        self.db.on_o_fail_depart = "fails to depart."

    def get_arrive(self):
        arrive_exit = is_none(self.obj.link.return_exit, self.obj)
        return self._get_message(arrive_exit.rp.db.on_success_arrive)

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
            self.db.on_o_fail_depart,
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


class ExitControlHandler(Handler):
    DB_HANDLER_NAME = "exit_access_handler"

    OPTION_CLOSE = 0b1
    OPTION_LOCK = 0b10
    OPTION_SEAL = 0b100

    STATE_OPENED = 0b1
    STATE_CLOSED = 0b10

    # [STATE_CLOSED (Close), STATE_COLLAPSED (Destroyed)]
    # # [STATE_OPEN (Open), STATE_LOCKED (Lock), STATE_COLLAPSED (Destroyed),
    # #  STATE_BREACHED (Destroyed)]
    # STATE_COLLAPSED = 1
    # # [STATE_OPEN (Clear/Repair)]
    # STATE_SEALED = 1
    # STATE_LOCKED = 1
    # STATE_CLOSED = 1
    # STATE_BREACHED = 1, [STATE_OPEN]

    def __init__(self, exit_obj):
        super(ExitControlHandler, self).__init__(exit_obj)
        # TODO: Delete
        del self.db.initialized

    def at_handler_creation(self):
        self.db.options = 0
        self.db.state = 0

        self.db.on_open = "You open the doors."
        self.db.on_o_open = "opens the doors."

        self.db.on_close = "You close the doors."
        self.db.on_o_close = "closes the doors."

        self.db.on_unlock = "You unlock the doors."
        self.db.on_o_unlock = "unlocks the doors."

        self.db.on_lock = "You lock the doors."
        self.db.on_o_lock = "locks the doors."

    # region Flags
    def can_close(self):
        return bits.isset(self.db.options, self.OPTION_CLOSE)

    def can_lock(self):
        return bits.isset(self.db.options, self.OPTION_LOCK)

    def can_seal(self):
        return bits.isset(self.db.options, self.OPTION_SEAL)

    def is_closed(self):
        return bits.isset(self.db.state, self.OPTION_CLOSE)

    def is_locked(self):
        return bits.isset(self.db.state, self.OPTION_LOCK)

    def is_sealed(self):
        return bits.isset(self.db.state, self.OPTION_SEAL)

    def upgrade(self, flag):
        self.db.options = bits.set(self.db.options, flag)

    def downgrade(self, flag):
        self.db.options = bits.unset(self.db.options, flag)

    # endregion

    def open(self, caller):
        # TODO: Jason
        self.set_lock("traverse:true()")
        caller.msg("Opening exit.")

    def close(self, caller):
        # TODO: Jason
        self.set_lock("traverse:false()")
        caller.msg("Closing exit.")

    def set_lock(self, lockstring):
        self.obj.locks.add(lockstring)
        self.obj.return_exit.locks.add(lockstring)
