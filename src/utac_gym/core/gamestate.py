from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from .types import GAMESTATE


class GameState:
    """
    A Python interface for the C++ GameState class.
    """

    def __init__(self, gs: Optional[GAMESTATE] = None):
        """Initialize the game state."""
        pass

    def make_move(self, action: int) -> None:
        """Make a move in the game.

        Args:
            action: The action to take
        """
        pass

    def get_obs(self) -> List[float]:
        """Get the current observation of the game state.

        Returns:
            List of floating point values representing the game state
        """
        pass

    def get_valid_moves(self) -> List[int]:
        """Get list of valid moves in current state.

        Returns:
            List of valid move indices
        """
        pass

    def get_valid_mask(self) -> List[bool]:
        """Get a boolean mask of valid moves.

        Returns:
            Boolean list where True indicates valid moves
        """
        pass

    def is_terminal(self) -> bool:
        """Check if current state is terminal.

        Returns:
            True if game is over, False otherwise
        """
        pass

    def terminal_value(self) -> float:
        """Get the terminal value if game is over.

        Returns:
            Final score/value of the terminal state
        """
        pass

    def current_player(self) -> int:
        """Get the current player.

        Returns:
            The current player
        """
        pass

    def _get_gs(self) -> GAMESTATE:
        """Get the underlying C++ GameState object.

        Returns:
            The underlying C++ GameState object
        """
        pass


if not TYPE_CHECKING:
    from utac_gym._core import State as CppState

    GameState = CppState

__all__ = ["GameState"]
