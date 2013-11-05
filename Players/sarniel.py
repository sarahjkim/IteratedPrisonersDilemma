import Game

class Player():

    START_BREATH_TEST = 21

    def __init__(self, _scoreboard, _ID):
        self.scoreboard = _scoreboard
        self.ID = _ID

        self.current_round = 0
        self.drunken_count = 0
        # self.our_choices = []
        # self.reaction_dict = {}

        self.last_true_move = None

    def get_move(self):
        self.current_round = self.scoreboard.get_round_number()

        self.update_drunken_count()
        result_move = self.main_decision()

        self.last_true_move = self.check_drunkeness(result_move)

        return self.last_true_move

    def update_drunken_count(self):
        if not self.last_true_move:
            return

        if self.last_true_move != self.scoreboard.get_player_move(self.current_round - 1, self.ID):
            self.drunken_count += 1

    def main_decision(self):
        return Game.RAT_OUT

    def check_drunkeness(self, move):
        if self.current_round >= self.START_BREATH_TEST and self.lawyer_is_drunk():
           return Game.opposite_move(move)
        return move

    def lawyer_is_drunk(self):
        return self.get_drunken_percent() >= 0.5

    def get_drunken_percent(self):
        return self.drunken_count / (self.current_round)
