from random import randrange

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

        animated_sprite.animation = mob_types[randrange(len(mob_types))]

    def _on_VisibilityNotifier2D_screen_exited(self):
        self.queue_free()
