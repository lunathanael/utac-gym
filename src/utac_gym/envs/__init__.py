from . import utacenv
from .utacenv import UtacEnv
from gymnasium import register

register(
    id="utac-v0",
    entry_point="utac_gym.envs:UtacEnv",
)

__all__ = ["UtacEnv"]
