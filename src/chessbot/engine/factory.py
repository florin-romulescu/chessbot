from enum import Enum

from .engine import ChessEngine
from .minimax import MinimaxEngine


class EngineType(Enum):
    MINIMAX = "minimax"


class EngineFactory:
    engines = {EngineType.MINIMAX: MinimaxEngine()}

    @staticmethod
    def get_engine(engine_type: EngineType) -> ChessEngine:
        return EngineFactory.engines[engine_type]
