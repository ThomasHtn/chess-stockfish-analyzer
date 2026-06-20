"""Stockfish analysis helpers."""

from __future__ import annotations

import chess
import chess.engine

from src.config import STOCKFISH_PATH


def analyze_position(
    board: chess.Board,
    depth: int,
    multipv: int,
) -> list[chess.engine.InfoDict]:
    """Analyze the current board position with Stockfish.

    Args:
        board: Current chess position.
        depth: Stockfish search depth.
        multipv: Number of candidate moves to return.

    Returns:
        A list of Stockfish analysis dictionaries.
    """

    if not STOCKFISH_PATH.exists():
        raise FileNotFoundError(f"Stockfish not found: {STOCKFISH_PATH}")

    with chess.engine.SimpleEngine.popen_uci(str(STOCKFISH_PATH)) as engine:
        return engine.analyse(
            board,
            chess.engine.Limit(depth=depth),
            multipv=multipv,
        )


def format_score(score: chess.engine.PovScore) -> str:
    """Convert a Stockfish score into a human-readable value.

    Examples:
        +0.45 means a small advantage.
        -1.20 means a disadvantage.
        Mate in 3 means a forced mate sequence.
    """

    relative = score.relative

    if relative.is_mate():
        mate = relative.mate()

        if mate is None:
            return "Mate"

        return f"Mate in {mate}" if mate > 0 else f"Mated in {abs(mate)}"

    centipawns = relative.score()

    if centipawns is None:
        return "Unknown"

    return f"{centipawns / 100:+.2f}"
