from random import randint

from godot import (
    exposed,
    export,
    RigidBody2D,
)


@exposed
class Mob(RigidBody2D):

    min_speed = export(int, default=150)  # Minimum speed range.
    max_speed = export(int, default=250)  # Maximum speed range.

    def _ready(self):
        animated_sprite = self.get_node("AnimatedSprite")

        mob_types = animated_sprite.frames.get_animation_names()
        animated_sprite.animation = mob_types[randint(0, len(mob_types)-1)]

    def _on_VisibilityNotifier2D_screen_exited(self):
        # NOTE: I'm not sure what the method name for this yet.
        self.queue_free()
