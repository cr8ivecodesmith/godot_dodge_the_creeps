from godot import (
    exposed,
    Area2D,
    Vector2,
    Input,
)

from utils import clamp


@exposed
class Player(Area2D):
    speed = 420
    screen_size = None

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

        if velocity.length() > 0:
            velocity = velocity.normalized() * self.speed
            self.get_node("AnimatedSprite").play()
        else:
            self.get_node("AnimatedSprite").stop()

        self.position += velocity * delta

        # NOTE: It seems you can't set the self.position's x and y values
        # so you'll need to assign a new vector instead.
        self.position = Vector2(
            clamp(self.position.x, 0, self.screen_size.x),
            clamp(self.position.y, 0, self.screen_size.y),
        )

        if velocity.x != 0:
            self.get_node("AnimatedSprite").animation = "walk"
            self.get_node("AnimatedSprite").flip_v = False
            self.get_node("AnimatedSprite").flip_h = velocity.x < 0
        elif velocity.y != 0:
            self.get_node("AnimatedSprite").animation = "up"
            self.get_node("AnimatedSprite").flip_v = velocity.y > 0
