from godot import (
    exposed,
    CanvasLayer,
    signal,
)


@exposed
class Hud(CanvasLayer):
    start_game = signal()
    is_game_over = False
    show_start_button = False

    def show_message(self, text):
        message = self.get_node("Message")
        message.text = text
        message.show()
        self.get_node("MessageTimer").start()

    def show_game_over(self):
        self.show_message("Game Over")
        self.is_game_over = True

    def show_title_message(self):
        message = self.get_node("Message")
        message.text = "Dodge the\nCreeps!"
        message.show()
        self.get_node("DelayTimer").start()
        self.show_start_button = True

    def update_score(self, score):
        self.get_node("ScoreLabel").text = str(score)

    def _on_StartButton_pressed(self):
        self.get_node("StartButton").hide()
        self.call('emit_signal', 'start_game')

    def _on_MessageTimer_timeout(self):
        self.get_node("Message").hide()

        if self.is_game_over:
            self.is_game_over = False
            self.show_title_message()

    def _on_DelayTimer_timeout(self):
        if self.show_start_button:
            self.show_start_button = False
            self.get_node("StartButton").show()
