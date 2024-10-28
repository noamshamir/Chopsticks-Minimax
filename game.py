import copy
from player import Player
import time

class Game():
    def __init__(self, player1_type, player2_type, l1=1, r1=1, l2=1, r2=1, turn='Player 1'):
        self.player1 = Player(player1_type, l1, r1)
        self.player2 = Player(player2_type, l2, r2)
        self.turn = turn
        self.score = None
        if not self.player1.is_alive and not self.player2.is_alive:
            raise ValueError("Cannot initialize game with both players dead, c'mon man")
        if not self.player1.is_alive:
            self.winner = 'Player 2'
        elif not self.player2.is_alive:
            self.winner = 'Player 1'
        else:
            self.winner = None
        self.positions = [self.key()]
        self.solved_positions = {}

    def to_string(self):
        return f"{self.player1.left_hand.fingers}{self.player1.right_hand.fingers}{self.player2.left_hand.fingers}{self.player2.right_hand.fingers}"
    
    def print(self):
        print(self.to_string())
    
    def print_status(self):
        print(f"Player 1: Left hand: {self.player1.left_hand.fingers} | Right hand: {self.player1.right_hand.fingers}")
        print(f"Player 2: Left hand: {self.player2.left_hand.fingers} | Right hand: {self.player2.right_hand.fingers}")
        print(f"Turn: {self.turn}")
        if self.winner is not None:
            print(f"Winner: {self.winner}")
    
    def move(self, action_type, attacking_hand_str, attacked_hand_str, simulate=False):
        if action_type != 'attack':
            raise ValueError('Undefined attack type')

        self.attack(self.attacking_player(), self.attacked_player(), attacking_hand_str, attacked_hand_str, simulate)
        
        if not self.player1.is_alive:
            self.winner = 'Player 2'
            if not simulate:
                print('Player 2 wins!')
        elif not self.player2.is_alive:
            self.winner = 'Player 1'
            if not simulate:
                print('Player 1 wins!')
        elif self.player1.is_alive and self.player2.is_alive:
            self.winner = None
        else:
            raise ValueError("Invalid is_alive for some player.")
        
        if self.key() in self.positions:
            self.winner = 'Tie'
            if not simulate:
                print('Game Ties!')
                
        self.positions.append(self.key())      

    def attack(self, attacking_player, attacked_player, attacking_hand_str, attacked_hand_str, simulate=False):
        
        if attacking_hand_str == 'r':
            attacking_hand = attacking_player.right_hand
        elif attacking_hand_str == 'l':
            attacking_hand = attacking_player.left_hand
        else:
            raise ValueError('Invalid attacking hand input')
        
        if attacked_hand_str == 'r':
            attacked_hand = attacked_player.right_hand
        elif attacked_hand_str == 'l':
            attacked_hand = attacked_player.left_hand
        else:
            raise ValueError('Invalid attacking hand input')

        if not attacking_hand.is_alive or not attacked_hand.is_alive:
            raise ValueError('Attacking dead hand or with dead hand')
        
        attacked_player.receive_attack(attacking_hand.fingers, attacked_hand_str)
        
        if not simulate:
            print(f"{self.turn} is attacking with {attacking_hand_str.upper()} hand ({attacking_hand.fingers} fingers) "
                  f"against {('Player 2' if self.turn == 'Player 1' else 'Player 1')}'s {attacked_hand_str.upper()} hand.")     

    def get_alive_hands(self):
        alive_attacking_hands = []
        if self.attacking_player().left_hand.is_alive:
            alive_attacking_hands.append('l')
        if self.attacking_player().right_hand.is_alive:
            alive_attacking_hands.append('r')

        alive_attacked_hands = []
        if self.attacked_player().left_hand.is_alive:
            alive_attacked_hands.append('l')
        if self.attacked_player().right_hand.is_alive:
            alive_attacked_hands.append('r')
            
        return alive_attacking_hands, alive_attacked_hands
    
    def create_next_generation(self):
        next_generation_positions = []
        alive_attacking_hands, alive_attacked_hands = self.get_alive_hands()
            
        for attacking_hand_str in alive_attacking_hands:
            for attacked_hand_str in alive_attacked_hands:
                try:
                    game_copy = copy.deepcopy(self)
                    game_copy.move('attack', attacking_hand_str, attacked_hand_str, simulate=True)
                    next_generation_positions.append((game_copy.to_string(), ('attack', attacking_hand_str, attacked_hand_str)))
                except ValueError as e:
                    print(e)
        return next_generation_positions
    
    def attacking_player(self):
        if self.turn == 'Player 1':
            return self.player1
        else:
            return self.player2
        
    def attacked_player(self):
        if self.turn == 'Player 1':
            return self.player2
        else:
            return self.player1
    
    def start(self):
        while(True):
            self.play_turn()
            self.print_status()
            if self.winner is not None:
                print(f'{self.winner} wins')
                break
            
    def play_turn(self):
        if self.attacking_player().is_human:
            self.play_human_turn()
        else:
            self.play_computer_turn()
        self.turn = 'Player 1' if self.turn == 'Player 2' else 'Player 2'
    
    def play_human_turn(self):
        while True:
            attacking_hand_str = input(f'{self.turn}, attack with your left or right hand? (l/r)')
            attacked_hand_str = input(f'{self.turn}, attack other players left or right hand? (l/r)')
            try:
                self.move('attack', attacking_hand_str, attacked_hand_str)
                break
            except ValueError as e:
                print(e)
                
    def play_computer_turn(self):
        start_time = time.time()
        print(f"Computer Playing... Turn: {self.turn}")
        
        score, best_move = Game.minimax(self, self, self.turn)
    
        try:
            if best_move:
                action_type, attacking_hand_str, attacked_hand_str = best_move
                self.move(action_type, attacking_hand_str, attacked_hand_str)
                print(f"Computer chose to {action_type} with {attacking_hand_str} attacking {attacked_hand_str}")
                print(f"Predicted outcome from perspective of {self.turn}: {score}")
            else:
                print("No valid move found")
                
        except ValueError as e:
            print(e)
    
        end_time = time.time()
        computer_turn_time = end_time - start_time

    def key(self):
        return f'{self.to_string()}{self.turn}'
    
    def fully_reversed_key(self):
        return f'{self.player1.right_hand.fingers}{self.player1.left_hand.fingers}{self.player2.right_hand.fingers}{self.player2.left_hand.fingers}{self.turn}'
    
    def attacker_reversed_key(self):
        return f'{self.player1.right_hand.fingers}{self.player1.left_hand.fingers}{self.player2.left_hand.fingers}{self.player2.right_hand.fingers}{self.turn}'
    
    def attacked_reversed_key(self):
        return f'{self.player1.left_hand.fingers}{self.player1.right_hand.fingers}{self.player2.right_hand.fingers}{self.player2.left_hand.fingers}{self.turn}'
    
    def reversed_players_key(self):
        return f'{self.player2.left_hand.fingers}{self.player2.right_hand.fingers}{self.player1.left_hand.fingers}{self.player1.right_hand.fingers}'
       
    @staticmethod        
    def minimax(init_game, game, player_to_max, depth=0, visited_positions=None, is_maximizing=True):
        if visited_positions is None:
            visited_positions = []

        if game.winner is not None:            
            if player_to_max == game.winner:
                return 1, None
            elif game.winner == 'Tie':
                return 0, None
            else:
                return -1, None
        
        best_score = -2 if is_maximizing else 2
        best_move = None
        
        next_gen = game.create_next_generation()     
        for position, move in next_gen:
            
            new_game = Game(
                game.player1.player_type, game.player2.player_type, 
                int(position[0]), int(position[1]), int(position[2]), int(position[3]),
                'Player 1' if game.turn == 'Player 2' else 'Player 2'
            )
            
            if new_game.key() in visited_positions:
                score = 0
                best_move = None               
            else:            
                visited_positions_copy = copy.deepcopy(visited_positions)
                visited_positions_copy.append(new_game.key())
                
                if init_game.solved_positions.get(new_game.key()) is not None:
                    score, move = init_game.solved_positions[new_game.key()]               
                elif init_game.solved_positions.get(new_game.fully_reversed_key()) is not None:
                     score, unmodified_move = init_game.solved_positions[new_game.fully_reversed_key()]
                     move = (unmodified_move[0], 'r' if unmodified_move[1] == 'l' else 'l', 'r' if unmodified_move[2] == 'l' else 'l')                    
                elif init_game.solved_positions.get(new_game.attacker_reversed_key()) is not None:
                    score, unmodified_move = init_game.solved_positions[new_game.attacker_reversed_key()]
                    move = (unmodified_move[0], 'r' if unmodified_move[1] == 'l' else 'l', unmodified_move[2])
                elif init_game.solved_positions.get(new_game.attacked_reversed_key()) is not None:
                    score, unmodified_move = init_game.solved_positions[new_game.attacked_reversed_key()]
                    move = (unmodified_move[0], unmodified_move[1], 'r' if unmodified_move[2] == 'l' else 'l')                   
                elif init_game.solved_positions.get(new_game.reversed_players_key()) is not None:
                    opposite_score, move = init_game.solved_positions[new_game.reversed_players_key()]
                    score = -opposite_score        
                else:
                    score, _ = Game.minimax(init_game, new_game, player_to_max, depth + 1, visited_positions_copy, not is_maximizing)

                    init_game.solved_positions[new_game.key()] = (score, move)

            if is_maximizing and score > best_score:
                best_score = score
                best_move = move
            elif not is_maximizing and score < best_score:
                best_score = score
                best_move = move

        return best_score, best_move
