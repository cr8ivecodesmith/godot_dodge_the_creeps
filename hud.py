from godot import (
    exposed,
    CanvasLayer,
    signal,
)


@exposed
class Hud(CanvasLayer):
    start_game = signal()

    def show_message(self, text):
        message = self.get_node("Message")
        message.text = text
        message.show()
        self.get_node("MessageTimer").start()

    def show_game_over(self):
        self.show_message("Game Over")

        # TODO:
        # signal(self.get_node("MessageTimer"), "timeout")
        # wait for message timer to signal timeout

        message = self.get_node("Message")
        message.text = "Dodge the\nCreeps!"
        message.show()

        # TODO:
        # Make a one-shot timer and wait for it to finish.
        timer = self.get_tree().create_timer(1)
        # yield timer, "timeout"
        # wait for timer to signal timeout

        self.get_node("StartButton").show()

    def update_score(self, score):
        self.get_node("ScoreLabel").text = score

    def _on_StartButton_pressed(self):
        self.get_node("StartButton").hide()
        self.emit_signal("start_game")

    def _on_MessageTimer_timeout(self):
        self.get_node("Message").hide()
