from godot import (
    exposed,
    Area2D,
    Vector2,
    Input,
    signal,
)

from utils import clamp


@exposed
class Player(Area2D):
    speed = 420
    screen_size = None
    hit = signal()

    def _ready(self):
        self.screen_size = self.get_viewport_rect().size
        self.hide()

    def _process(self, delta):
        velocity = Vector2()

        if Input.is_action_pressed("ui_right"):
            velocity.x += 1
        if Input.is_action_pressed("ui_left"):
            velocity.x -= 1
        if Input.is_action_pressed("ui_down"):
            velocity.y += 1
        if Input.is_action_pressed("ui_up"):
            velocity.y -= 1

        animated_sprite = self.get_node("AnimatedSprite")
        if velocity.length() > 0:
            velocity = velocity.normalized() * self.speed
            animated_sprite.play()
        else:
            animated_sprite.stop()

        self.position += velocity * delta

        # NOTE: It seems you can't set the self.position's x and y values
        # so you'll need to assign a new vector instead.
        self.position = Vector2(
            clamp(self.position.x, 0, self.screen_size.x),
            clamp(self.position.y, 0, self.screen_size.y),
        )

        if velocity.x != 0:
            animated_sprite.animation = "walk"
            animated_sprite.flip_v = False
            animated_sprite.flip_h = velocity.x < 0
        elif velocity.y != 0:
            animated_sprite.animation = "up"
            animated_sprite.flip_v = velocity.y > 0

    def _on_Player_body_entered(self, body):
        self.hide()  # Player disappears after being hit.

        # NOTE: I'm not sure if this is the right method.
        self.emit_signal("hit")

        # Ensures that the collission shape is not disabled while
        # the Godot is still in the middle of collision processing.
        self.get_node("CollisionShape2D").set_deferred("disabled", True)

    def start(self, pos):
        self.position = pos
        self.show()
        self.get_node("CollisionShape2D").disabled = False
