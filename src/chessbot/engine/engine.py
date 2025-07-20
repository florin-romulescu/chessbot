from abc import ABC, abstractmethod
from typing import Optional

import chess


class ChessEngine(ABC):
    @abstractmethod
    def get_best_move(self, board: chess.Board) -> Optional[str]:
        pass
    
    @abstractmethod
    def get_move_with_time_limit(self, board: chess.Board, time_limit: float) -> Optional[str]:
        pass
    
    @abstractmethod
    def set_depth(self, depth: int) -> None:
        pass
    
    @abstractmethod
    def get_move(self, board: chess.Board, time_limit: Optional[float] = None) -> Optional[str]:
        pass