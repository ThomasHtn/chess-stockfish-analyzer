"""PGN parsing utilities."""

from __future__ import annotations

from io import StringIO

import chess
import chess.pgn


def read_game_from_pgn(pgn_text: str) -> chess.pgn.Game:
    """Parse a PGN string and return a python-chess Game object.

    The PGN can be copied directly from Chess.com. It may include headers such
    as Event, Site, Date, White, Black, ratings, time control, and an unfinished
    result marker.
    """

    game = chess.pgn.read_game(StringIO(pgn_text))

    if game is None:
        raise ValueError("Invalid or empty PGN.")

    return game


def build_board_from_game(game: chess.pgn.Game) -> chess.Board:
    """Rebuild the current board position from the PGN mainline.

    The board starts from the initial chess position, then every move from the
    mainline is applied in order.
    """

    board = game.board()

    for move in game.mainline_moves():
        board.push(move)

    return board
