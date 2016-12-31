"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """

    @property
    def last_exit(self):
        return self.ndb.last_exit

    @last_exit.setter
    def last_exit(self, value):
        self.ndb.last_exit = value

    @last_exit.deleter
    def last_exit(self):
        del self.ndb.last_exit

    def announce_move_from(self, destination):
        self._announce_depart(
            self.location,
            self.last_exit
        )

    def announce_move_to(self, source_location):
        # silence the announcement and shift it to after the move
        pass

    def at_after_move(self, source_location):
        super(Character, self).at_after_move(source_location)
        self._announce_arrive(
            self.location,
            self.last_exit
        )

    def _announce_depart(self, location, exit_obj):
        if exit_obj:
            for obj in location.contents:
                if obj == self:
                    obj.msg(exit_obj.rp.get_success_depart())
                else:
                    obj.msg(exit_obj.rp.get_o_success_depart(self, obj))
        else:
            for obj in location.contents:
                if obj != self:
                    obj.msg("{0} has disappeared.".format(
                        self.get_display_name(obj)))

    def _announce_arrive(self, location, exit_obj):
        if exit_obj:
            for content_obj in location.contents:
                if content_obj == self:
                    content_obj.msg(exit_obj.rp.get_arrive())
                else:
                    content_obj.msg(exit_obj.rp.get_o_arrive(self, content_obj))
        else:
            self.msg("Have Not")
            for content_obj in location.contents:
                if content_obj != self:
                    content_obj.msg("{0} has appeared.".format(
                        self.get_display_name(content_obj)))
