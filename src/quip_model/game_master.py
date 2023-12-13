import threading
import time
from random import shuffle, randint, sample

from .events import *
from .exceptions import *
from .player import Player, PlayerList
from .prompt import Prompt, PromptList
from .prompts_list import prompts

RESPONSE_COUNTDOWN = 60  # Time (in seconds) that the players have to respond to their prompts
VOTE_COUNTDOWN = 15  # Time (in seconds) that the players have to vote


class GameMaster:
    def __init__(self, observer: GameObserver):
        self.players = PlayerList()
        self.pending_players = PlayerList()  # Players that have connections but nothing else
        self.prompt_strs = prompts
        self.prompts = PromptList()
        self.round = 1
        self.observer = observer  # How we send events to the user
        self.timer = None
        self.is_playing = False

        self.responses_received = int()
        self.responses_received_lock = threading.Lock()

        self.votes_received = int()
        self.votes_received_lock = threading.Lock()

    def add_connection(self) -> int:
        random_id = randint(1, 10000)

        taken_nums = [player.id for player in self.players]
        taken_nums.extend([player.id for player in self.pending_players])

        # Prevents duplicate ID's
        while random_id in taken_nums:
            random_id = randint(1, 10000)

        # When player connects to game server, this is executed, player then needs to authenticate and enter their name
        self.pending_players.append(Player(random_id))  # Only add player to pending players list, name to be set later
        return random_id

    def accept_new_player(self, player_id: int, name: str):
        if self.players.has_player_by_name(name):  # Nicknames must be unique
            self.observer(NicknameAlreadyExistsEvent(player_id))
            raise PlayerNameAlreadyInUse(f"tried to use nickname already in use: {name}.")

        # Get player object
        player = self.pending_players.get_player_by_id(player_id)

        # Remove player from pending players list
        self.pending_players.remove_player_by_id(player_id)

        # Set player name
        player.name = name

        # If they are the first player, they become VIP
        if len(self.players) == 0:
            player.is_vip = True
            self.observer(PlayerVIPEvent(player_id))

        # Add player to player list
        self.players.append(player)

        # Send join event
        self.observer(PlayerJoinEvent(player_id))

    def _handle_vip_leave(self, player: Player):
        # Publish VIP leave event
        self.observer(VIPLeaveEvent(player.id))

        # Choose a new VIP
        for new_vip in self.players:
            print(f"trying {new_vip.name}")
            if new_vip.id == player.id:
                print("rejected")
                continue

            new_vip.is_vip = True
            self.observer(PlayerVIPEvent(new_vip.id))
            print("new vip made")
            break

    def remove_player(self, player_num: int):
        """
        Removes a player from the list of players in the game. Caused by player
        disconnecting from the game. If a player does not exist, an exception is
        thrown.

        Parameters:
            player_num (int): The number/id of the player to remove.
        """

        player_nums = [player.id for player in self.players]
        pending_player_nums = [player.id for player in self.pending_players.players]

        player_pending = False

        if player_num in player_nums:
            player = self.players.get_player_by_id(player_num)
        elif player_num in pending_player_nums:
            player = self.pending_players.get_player_by_id(player_num)
            player_pending = True
        else:
            raise PlayerDoesNotExist(f"Player {player_num} does not exist.")

        if player.is_vip:
            self._handle_vip_leave(player)

        if player_pending:
            self.pending_players.remove_player_by_id(player_num)
        else:
            self.players.remove_player_by_id(player_num)

    def _choose_two_prompts(self, player: Player, available_prompts: list[str],
                            prompt_pairings: dict[str, list[int]]) -> None:

        choices_made = 0

        while choices_made < 2:
            random_prompt = sample(available_prompts, k=1)[0]
            if player.id in prompt_pairings[random_prompt] or len(prompt_pairings[random_prompt]) == 2:
                continue

            empty_available = False

            for id_list in prompt_pairings.values():
                if len(id_list) == 0:
                    empty_available = True
                    break

            if empty_available and len(prompt_pairings[random_prompt]) != 0:
                continue

            prompt_pairings[random_prompt].append(player.id)
            choices_made += 1
            print(f"choices made: {choices_made}")

    def distribute_prompts(self) -> None:
        """
        Create prompt assignments and distribute them.
        """

        available_prompts = sample(list(self.prompt_strs), k=len(self.players))

        prompt_pairings = dict[str, list[int]]()

        for prompt in available_prompts:
            prompt_pairings[prompt] = list[int]()

        shuffle(self.players.players)

        for player in self.players.players:
            self._choose_two_prompts(player, available_prompts, prompt_pairings)

        for index, prompt in enumerate(prompt_pairings.keys()):
            prompt_object = Prompt(index, prompt, prompt_pairings[prompt])
            self.prompts.append(prompt_object)
            for player_id in prompt_pairings[prompt]:
                player = self.players.get_player_by_id(player_id)
                player.current_prompts.append(prompt_object)

        for player in self.players.players:
            self.observer(DistributePromptEvent(player.id,
                                                player.current_prompts[0].prompt,
                                                player.current_prompts[1].prompt,
                                                player.current_prompts[0].id,
                                                player.current_prompts[1].id))

    def calculate_points(self, prompt: Prompt) -> None:
        # Get player objects
        player_0 = self.players.get_player_by_id(prompt.player_ids[0])
        player_1 = self.players.get_player_by_id(prompt.player_ids[1])

        # Get the number of votes for each player
        player_0_votes = len(prompt.votes[player_0.id])
        player_1_votes = len(prompt.votes[player_1.id])

        # Get the names of the voters for each player
        player_0_voter_names = list[str]()
        for voter_num in prompt.votes[player_0.id]:
            voter = self.players.get_player_by_id(voter_num)
            player_0_voter_names.append(voter.name)

        player_1_voter_names = list[str]()
        for voter_num in prompt.votes[player_1.id]:
            voter = self.players.get_player_by_id(voter_num)
            player_1_voter_names.append(voter.name)

        # Determine if there was a tie
        total_votes = player_0_votes + player_1_votes
        tie = (total_votes == 0) or (player_0_votes == player_1_votes)

        winner = None
        quiplasher = None

        player_0_points_awarded = 0
        player_1_points_awarded = 0

        # If there was a tie, each player gets 500 points and there is no winner and no quiplasher
        if tie:
            player_0_points_awarded = 500 * self.round
            player_1_points_awarded = 500 * self.round
        else:
            player_0_points_awarded = int(1000.0 * self.round * float(player_0_votes / total_votes))
            player_1_points_awarded = int(1000.0 * self.round * float(player_1_votes / total_votes))

            if player_0_points_awarded == 0:
                player_1_points_awarded += 500 * self.round
                winner = player_1.name
                quiplasher = player_1.name
            elif player_1_points_awarded == 0:
                player_0_points_awarded += 500 * self.round
                winner = player_0.name
                quiplasher = player_0.name
            elif player_0_points_awarded > player_1_points_awarded:
                player_0_points_awarded += 100 * self.round
                winner = player_0.name
            elif player_1_points_awarded > player_0_points_awarded:
                player_1_points_awarded += 100 * self.round
                winner = player_1.name

        # Add the points to the players
        player_0.points += player_0_points_awarded
        player_1.points += player_1_points_awarded

        # Add the points to the event
        self.observer(EndPromptVotingEvent(player_0.name, player_0_voter_names, player_0_points_awarded,
                                           player_1.name, player_1_voter_names, player_1_points_awarded,
                                           tie, winner, quiplasher))

    def handle_scoreboard(self):
        # Gets the list of players sorted by descending points order
        sorted_players = sorted(self.players.players, key=lambda player: player.points, reverse=True)

        # Get separate lists of names and points from ordered list
        sorted_player_names = [player.name for player in sorted_players]
        sorted_player_points = [player.points for player in sorted_players]

        # Publish scoreboard event
        self.observer(ScoreboardEvent(sorted_player_names, sorted_player_points))

    def wait_for_responses(self):
        countdown = 60
        while countdown > 0:
            with self.responses_received_lock:
                if self.responses_received == len(self.players):
                    self.responses_received = 0
                    break
            countdown -= 1
            time.sleep(1)
        
        with self.responses_received_lock:
            self.responses_received = 0


    def wait_for_votes(self):
        countdown = 15
        while countdown > 0:
            with self.votes_received_lock:
                if self.votes_received == len(self.players) - 2:
                    self.votes_received = 0
                    break

            time.sleep(1)
            countdown -= 1
        with self.votes_received_lock:
            self.votes_received = 0
        self.observer(ClientEndPromptVotingEvent())

    def play_round(self):
        # Start the round
        self.observer(RoundStartedEvent(self.round))
        self.is_playing = True

        # Distribute prompts
        self.distribute_prompts()

        print("ALL PROMPTS DISTRIBUTED")

        # Wait for responses to come back
        self.wait_for_responses()

        time.sleep(2)

        print("ALL RESPONSES RECEIVED")

        self.observer(BeginVotingEvent(self.round))

        for prompt in self.prompts:
            # Start the voting for this prompt
            self.observer(BeginPromptVotingEvent(prompt))

            self.wait_for_votes()

            self.calculate_points(prompt)

            time.sleep(5)

            print("PROMPT VOTE DONE")

        self.handle_scoreboard()

        time.sleep(5)

        print("ALL VOTING DONE")
