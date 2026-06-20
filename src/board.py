"""Board rendering and candidate move table utilities."""

from __future__ import annotations

import chess
import chess.svg
import pandas as pd

from src.config import BOARD_COLORS, BOARD_SIZE
from src.engine import format_score


def get_board_orientation(board: chess.Board) -> chess.Color:
    """Choose the board orientation.

    The side to move is displayed at the bottom. This keeps the UI anonymous and
    avoids relying on player names.
    """

    return board.turn


def make_board_before_svg(
    board: chess.Board,
    best_move: chess.Move,
    orientation: chess.Color,
) -> str:
    """Generate the current board as SVG.

    A red arrow is drawn from the best move origin square to its target square.
    """

    return chess.svg.board(
        board=board,
        orientation=orientation,
        arrows=[
            chess.svg.Arrow(
                best_move.from_square,
                best_move.to_square,
                color="#ef4444",
            )
        ],
        size=BOARD_SIZE,
        colors=BOARD_COLORS,
    )


def make_board_after_svg(
    board: chess.Board,
    best_move: chess.Move,
    orientation: chess.Color,
) -> str:
    """Generate the board after applying Stockfish's best move.

    The destination square is highlighted as the last move.
    """

    next_board = board.copy()
    next_board.push(best_move)

    return chess.svg.board(
        board=next_board,
        orientation=orientation,
        lastmove=best_move,
        size=BOARD_SIZE,
        colors=BOARD_COLORS,
    )


def build_candidates_table(
    board: chess.Board,
    infos: list[chess.engine.InfoDict],
) -> pd.DataFrame:
    """Build a compact table containing Stockfish candidate moves.

    SAN is the human chess notation, such as Nf3, e4, O-O. UCI is the engine
    notation, such as g1f3, e2e4.
    """

    rows = []

    for rank, info in enumerate(infos, start=1):
        move = info["pv"][0]

        rows.append(
            {
                "#": rank,
                "Move": board.san(move),
                "UCI": str(move),
                "Score": format_score(info["score"]),
            }
        )

    return pd.DataFrame(rows)
