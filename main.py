from math import pi
from random import random, uniform, randint

from godot import (
    exposed,
    Node,
    ResourceLoader,
    Vector2,
)


@exposed
class Main(Node):
    # NOTE: Exporting a PackedScene object doesn's seem to work
    # so we'll load the resource directly.
    Mob = ResourceLoader.load("res://Mob.tscn", "PackedScene", False)

    score = 0

    def _ready(self):
        return

    def game_over(self):
        self.get_node("ScoreTimer").stop()
        self.get_node("MobTimer").stop()

        self.get_node("HUD").show_game_over()

        # Call the queue_free function in every node belonging to the
        # mobs group.
        self.get_tree().call_group("mobs", "queue_free")
        self.get_node("Music").stop()
        self.get_node("DeathSound").play()

    def new_game(self):
        self.score = 0
        self.get_node("Player").start(
            self.get_node("StartPosition").position
        )
        self.get_node("StartTimer").start()

        hud = self.get_node("HUD")
        hud.update_score(self.score)
        hud.show_message("Get Ready")

        self.get_node("Music").play()

    def _on_StartTimer_timeout(self):
        self.get_node("MobTimer").start()
        self.get_node("ScoreTimer").start()

    def _on_ScoreTimer_timeout(self):
        self.score += 1
        self.get_node("HUD").update_score(self.score)

    def _on_MobTimer_timeout(self):
        mob_spawn_location = self.get_node("MobPath/MobSpawnLocation")

        # Choose a random location on Path2D
        # NOTE: Since there's no randi, we'll approximate a random location
        # between 0-1000
        mob_spawn_location.offset = random() * 1000

        # Create a mob instance and add it to the scene
        mob = self.Mob.instance()
        self.add_child(mob)

        # Set the mob's direction perpendicular to the path direction.
        direction = mob_spawn_location.rotation + pi / 2

        # Set the mob's position to a random location.
        mob.position = mob_spawn_location.position

        # Add some radomness to the direction.
        direction += uniform(-pi / 4, pi / 4)
        mob.rotation = direction

        # Set the velocity (speed and direction).
        mob.linear_velocity = Vector2(
            randint(mob.min_speed, mob.max_speed), 0
        )
        mob.linear_velocity = mob.linear_velocity.rotated(direction)
