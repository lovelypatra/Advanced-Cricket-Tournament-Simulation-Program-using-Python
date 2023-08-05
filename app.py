import random
from exception import CricketException
import sys
from logger import logging

try:

    class Player:
        def __init__(self, name, batting, bowling, fielding, running, experience):
            self.name = name
            self.batting = batting
            self.bowling = bowling 
            self.fielding = fielding
            self.running = running
            self.experience = experience

    class Teams:
        def __init__(self, name):
            self.name = name
            self.players = []
            self.captain = None
            self.batting_order = []
            self.bowlers = []
            self.score = 0

        def select_captain(self):
            self.captain = random.choice(self.players)
        
        def add_player(self, player):
            self.players.append(player)
            logging.info(f"Add player to the batting order list only if they have not batted in the current innings")
            if player not in self.batting_order:
                self.batting_order.append(player)
            logging.info(f"Add player to the list of bowlers if they have a bowling rating greater than 0")
            if player.bowling > 0:
                self.bowlers.append(player)

        def send_next_player(self):
            if not self.batting_order:
                raise IndexError("Batting order is empty")
            return self.batting_order.pop(0)

        def choose_bowler(self):
            if not self.bowlers:
                raise IndexError("No bowlers available")
            return random.choice(self.bowlers)

    class Field:
        def __init__(self, field_size, fan_ratio, pitch_conditions, home_advantage):
            self.field_size = field_size
            self.fan_ratio = fan_ratio
            self.pitch_conditions = pitch_conditions
            self.home_advantage = home_advantage

    class Umpire:
        def __init__(self):
            self.score = 0
            self.wickets = 0
            self.overs = 0

        def predict_ball_outcome(self, batsman, bowler):
            logging.info(f"Randomly determine runs or wicket based on player stats")
            runs_prob = batsman.batting * bowler.bowling
            if random.random() < runs_prob:
                runs_scored = random.randint(0, 6)
                return "runs", runs_scored
            else:
                return "wicket", "batsman out"

        def handle_no_ball(self):
            logging.info(f"Simplified handling of no-ball scenario: Add an extra run to the batting team")
            self.score += 1

        def handle_wide_ball(self):
            logging.info(f"Simplified handling of wide-ball scenario: Add an extra run to the batting team")
            self.score += 1

        def handle_catch(self):
            logging.info(f"Simulate catching scenarios based on fielding skills")
            fielding_player = random.choice(self.current_bowling_team.players)
            catching_prob = fielding_player.fielding * 0.8
            is_catch_successful = random.random() <= catching_prob

            if is_catch_successful:
                batsman_out = self.current_batting_team.current_batsman
                self.umpire.update_wicket(batsman_out)
                self.commentator.comment(f"OUT! {batsman_out.name} caught by {fielding_player.name}.")
            else:
                self.commentator.comment("Catch Dropped!")


    class Commentator:
        def __init__(self, match):
            self.match_stats = match

        def provide_commentary(self):
            logging.info(f"Implement commentary based on match statistics.")
            if self.match_stats.score == 0:
                self.comment("A quiet start to the innings.")
            elif self.match_stats.score % 50 == 0:
                self.comment(f"Fifty up for {self.match_stats.current_batting_team.name}.")
            elif self.match_stats.score % 100 == 0:
                self.comment(f"Century for {self.match_stats.current_batting_team.name}.")
            elif self.match_stats.wickets == 1:
                self.comment("First wicket down!")
            elif self.match_stats.wickets % 2 == 0:
                self.comment(f"Another one bites the dust! {self.match_stats.wickets} down.")
            elif self.match_stats.wickets == len(self.match_stats.current_batting_team.players):
                self.comment(f"All out! {self.match_stats.current_batting_team.name} innings over.")

            logging.info(f"Additional comment for T20 and ODI formats when chasing")
            if self.match_stats.match_format in ["T20", "ODI"] and self.match_stats.target != -1:
                runs_required = self.match_stats.target - self.match_stats.score
                balls_remaining = (self.match_stats.match_format * 6) - (self.match_stats.overs * 10)
                if runs_required > 0:
                    self.comment(f"{runs_required} runs required from {balls_remaining} balls.")

        def comment(self, message):
            print(f"Commentary: {message}")

    class Match:
        def __init__(self, team_a, team_b, field):
            self.team_a = team_a
            self.team_b = team_b
            self.field = field
            self.umpire = Umpire()
            self.current_batting_team = None
            self.current_bowling_team = None
            self.score = {team_a: 0, team_b: 0}  
            logging.info(f"Create Dictionary to keep track of scores for each team")
            self.wickets = 0
            self.overs = 0

        def start_match(self):
            self.toss()
            self.play_match()

        def toss(self):
            logging.info(f"Simulate toss and decide which team bats first")
            toss_winner = random.choice([self.team_a, self.team_b])
            self.current_batting_team = toss_winner
            self.current_bowling_team = self.team_a if toss_winner == self.team_b else self.team_b
            print(f"{toss_winner.name} won the toss and elected to bat first.")

        def change_innings(self):
            logging.info(f"Switch innings after one team completes batting.")
            self.current_batting_team, self.current_bowling_team = self.current_bowling_team, self.current_batting_team
            print("\nInnings Change\n")

        def end_match(self):
            logging.info(f"End the match and declare the result.")
            match_result = "Match Drawn" if self.team_a.score == self.team_b.score else f"{self.team_a.name} Wins" if self.team_a.score > self.team_b.score else f"{self.team_b.name} Wins"
            print(f"\nMatch Result: {match_result}\n")

        def simulate_ball(self, batsman, bowler):
            ball_outcome_type, ball_outcome = self.umpire.predict_ball_outcome(batsman, bowler)
            if ball_outcome_type == "runs":
                self.score += ball_outcome
            elif ball_outcome_type == "wicket":
                self.wickets += 1
                if self.wickets == len(self.current_batting_team.players):
                    self.change_innings()

        def handle_no_ball(self):
            self.umpire.handle_no_ball()

        def handle_wide_ball(self):
            self.umpire.handle_wide_ball()

        def play_match(self):
            num_overs = 20  
            logging.info(f"Assuming a T20 match for simplicity")

            while self.overs < num_overs:
                try:
                    current_batsman = self.current_batting_team.send_next_player()
                except IndexError:
                    print(f"\nAll out! {self.current_batting_team.name} innings over.\n")
                if self.current_batting_team == self.team_a:
                    if self.team_b.batting_order:
                        self.change_innings()
                    else:
                        logging.info(f"Both teams have finished batting, end the match")
                        break  
                else:
                    logging.info(f"Both teams have finished batting, end the match")
                    break  
                continue
                try:
                    current_bowler = self.current_bowling_team.choose_bowler()
                except IndexError:
                    print(f"\nNo bowlers available for {self.current_bowling_team.name}.")
                    logging.info(f"End the match prematurely due to lack of bowler")
                    break  

                print(f"\nOver: {int(self.overs) + 1}, Ball: {int((self.overs - int(self.overs)) * 6) + 1}")
                self.simulate_ball(current_batsman, current_bowler)
                self.overs += 0.1
            self.end_match()

    def simulate_match(team_a, team_b, field):
        match = Match(team_a, team_b, field)
        match.start_match()

    def create_team(name):
        team = Teams(name)
        num_players = int(input(f"Enter the number of players for {name}: "))
        for _ in range(num_players):
            player_name = input(f"Enter player name: ")
            player_batting = float(input(f"Enter batting rating (0.0 - 1.0): "))
            player_bowling = float(input(f"Enter bowling rating (0.0 - 1.0): "))
            player_fielding = float(input(f"Enter fielding rating (0.0 - 1.0): "))
            player_running = float(input(f"Enter running rating (0.0 - 1.0): "))
            player_experience = float(input(f"Enter experience rating (0.0 - 1.0): "))
            team.add_player(Player(player_name, player_batting, player_bowling, player_fielding, player_running, player_experience))
        return team

    def main():
        match_format = input("Enter match format (T20, ODI, Test): ")
        field_size = float(input("Enter field size (0.0 - 1.0): "))
        fan_ratio = float(input("Enter fan ratio (0.0 - 1.0): "))
        pitch_conditions = float(input("Enter pitch conditions (0.0 - 1.0): "))
        home_advantage = float(input("Enter home advantage (0.0 - 1.0): "))
        team_a = create_team("Team A")
        team_b = create_team("Team B")

        field = Field(field_size, fan_ratio, pitch_conditions, home_advantage)

        simulate_match(team_a, team_b, field)
   

    if __name__ == "__main__":
        main()
except Exception as e:
    raise CricketException(e, sys)