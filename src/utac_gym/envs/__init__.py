from . import utacenv
from .utacenv import UtacEnv
from gymnasium import register

register(
    id="utac-v0",
    entry_point="utac.envs:UtacEnv",
)

__all__ = ["UtacEnv"]
