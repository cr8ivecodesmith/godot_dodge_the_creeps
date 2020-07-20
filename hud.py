from godot import (
    exposed,
    CanvasLayer,
    signal,
)


@exposed
class Hud(CanvasLayer):
    start_game = signal()
    is_game_over = False

    def show_message(self, text):
        message = self.get_node("Message")
        message.text = text
        message.show()
        self.get_node("MessageTimer").start()

    def show_game_over(self):
        self.show_message("Game Over")
        self.is_game_over = True

    def update_score(self, score):
        self.get_node("ScoreLabel").text = str(score)

    def _on_StartButton_pressed(self):
        self.get_node("StartButton").hide()
        self.call('emit_signal', 'start_game')

    def _on_MessageTimer_timeout(self):
        self.get_node("Message").hide()

        # This is call callback hack since I can't figure out
        # how to use the yield function in GDScript to wait and listen
        # to a signal
        if self.is_game_over:
            self.is_game_over = False

            message = self.get_node("Message")
            message.text = "Dodge the\nCreeps!"
            message.show()
            self.get_node("StartButton").show()
