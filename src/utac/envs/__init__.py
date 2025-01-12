from . import utacenv, utils, wrappers
from .utacenv import UtacEnv
from gymnasium import register
from .wrappers import InfoWrapper

register(
    id="utac-v0",
    entry_point="utac.envs:UtacEnv",
)

__all__ = ["utacenv", "utils", "wrappers", "UtacEnv", "InfoWrapper"]
