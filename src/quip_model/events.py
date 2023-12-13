from dataclasses import dataclass
from typing import Union, Callable

from quip_model.prompt import Prompt


@dataclass(eq=True, frozen=True)
class PlayerJoinEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class PlayerLeaveEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class VIPLeaveEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class PlayerNicknameEvent:
    player_num: int
    name: str


@dataclass(eq=True, frozen=True)
class PlayerResponseEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class PlayerVoteEvent:
    nickname: str
    vote: int


@dataclass(eq=True, frozen=True)
class PlayerVIPEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class RoundStartedEvent:
    round_num: int


@dataclass(eq=True, frozen=True)
class DistributePromptEvent:
    player_num: int
    prompt_0: str
    prompt_1: str
    prompt_0_id: int
    prompt_1_id: int


@dataclass(eq=True, frozen=True)
class StopAnsweringPrompts:
    pass


@dataclass(eq=True, frozen=True)
class BeginVotingEvent:
    round: int


@dataclass(eq=True, frozen=True)
class BeginPromptVotingEvent:
    prompt: Prompt


@dataclass(eq=True, frozen=True)
class ClientEndPromptVotingEvent:
    pass


@dataclass(eq=True, frozen=True)
class EndPromptVotingEvent:
    player_0_name: str
    player_0_voter_names: list[str]
    player_0_points_awarded: int

    player_1_name: str
    player_1_voter_names: list[str]
    player_1_points_awarded: int

    tie: bool
    # Winner and quiplasher are only set if there was a win or a quiplash
    winner: str
    quiplasher: str


@dataclass(eq=True, frozen=True)
class ScoreboardEvent:
    names_in_order: list[str]
    points_in_order: list[int]

@dataclass(eq=True, frozen=True)
class NicknameAlreadyExistsEvent:
    player_num: int


@dataclass(eq=True, frozen=True)
class GameFullEvent:
    game_id: int


GameEvent = Union[
    PlayerJoinEvent, PlayerLeaveEvent, PlayerResponseEvent, PlayerVoteEvent, PlayerVIPEvent,
    PlayerNicknameEvent, RoundStartedEvent, DistributePromptEvent, BeginVotingEvent,
    BeginPromptVotingEvent, EndPromptVotingEvent, VIPLeaveEvent, ScoreboardEvent, ClientEndPromptVotingEvent,
    NicknameAlreadyExistsEvent]

GameObserver = Callable[[GameEvent], None]
