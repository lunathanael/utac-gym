import numpy as np

from typing import Literal

Board = np.ndarray[tuple[Literal[9], Literal[9]], np.dtype[np.bool_]]
SubBoard = np.ndarray[tuple[Literal[3], Literal[3]], np.dtype[np.bool_]]
