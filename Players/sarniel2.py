import Game

class Player():

    START_BREATH_TEST = 21

    def __init__(self, _scoreboard, _ID):
        self.scoreboard = _scoreboard
        self.ID = _ID

        self.current_round = 0
        self.drunken_count = 0
        self.reaction_dict = {}

        self.last_true_move = None

    def get_move(self):
        self.current_round = self.scoreboard.get_round_number()

        self.update_drunken_count()
        self.update_reaction_dict()

        result_move = self.main_decision()
        self.last_true_move = self.check_drunkeness(result_move)

        return self.last_true_move

    def update_drunken_count(self):
        if not self.last_true_move:
            return

        if self.last_true_move != self.scoreboard.get_player_move(self.current_round - 1, self.ID):
            self.drunken_count += 1

    def update_reaction_dict(self):
        if self.current_round == 0:
            self.init_reaction_dict()
        else:
            # round 1 and so on
            previous_move_ours = self.scoreboard.get_player_move(self.current_round - 1, self.ID)
            previous_move_theirs = self.scoreboard.get_other_player_move(self.current_round - 1, self.ID)

            if previous_move_ours == Game.RAT_OUT:
                if previous_move_theirs == Game.RAT_OUT:
                    self.reaction_dict["RR"] += 1
                else:
                    self.reaction_dict["RS"] += 1
            else:
                if previous_move_theirs == Game.RAT_OUT:
                    self.reaction_dict["SR"] += 1
                else:
                    self.reaction_dict["SS"] += 1

    def get_reaction_percentage(self, key):
        if key == "RR" or key == "RS":
            return self.reaction_dict[key] / (self.reaction_dict["RR"] + self.reaction_dict["RS"])
        return self.reaction_dict[key] / (self.reaction_dict["SR"] + self.reaction_dict["SS"])

    def init_reaction_dict(self):
        self.reaction_dict["RR"] = 0
        self.reaction_dict["RS"] = 0
        self.reaction_dict["SR"] = 0
        self.reaction_dict["SS"] = 0

    def main_decision(self):
        if self.last_true_move == Game.STAY_SILENT:
            if self.get_reaction_percentage("SR") > self.get_reaction_percentage("SS"):
                return Game.RAT_OUT
        return Game.RAT_OUT

    def check_drunkeness(self, move):
        if self.current_round >= self.START_BREATH_TEST and self.lawyer_is_drunk():
           return Game.opposite_move(move)
        return move

    def lawyer_is_drunk(self):
        return self.get_drunken_percent() >= 0.5

    def get_drunken_percent(self):
        return self.drunken_count / (self.current_round)
