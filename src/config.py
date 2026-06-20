"""Application-wide configuration.

This module centralizes constants and environment-based settings so the rest of
application does not need to know where Stockfish is installed or how the board
should be styled.
"""

from __future__ import annotations

import os
from pathlib import Path

# Root directory of the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Stockfish executable path.
#
# Priority:
# 1. STOCKFISH_PATH environment variable, useful for Docker and deployment.
# 2. A local binary inside ./stockfish, useful for local development.
# 3. Debian/Ubuntu package default path, useful inside the provided Dockerfile.
STOCKFISH_PATH = Path(
    os.getenv(
        "STOCKFISH_PATH",
        BASE_DIR / "stockfish" / "stockfish-ubuntu-x86-64-avx2",
    )
)

if not STOCKFISH_PATH.exists():
    STOCKFISH_PATH = Path("/usr/games/stockfish")

if not STOCKFISH_PATH.exists():
    raise FileNotFoundError(
        "Stockfish executable not found. Set STOCKFISH_PATH or install Stockfish."
    )


# Default Stockfish analysis settings.
DEFAULT_DEPTH = 30
DEFAULT_MULTIPV = 5

# UI slider limits.
MIN_DEPTH = 8
MAX_DEPTH = 40
MIN_MULTIPV = 1
MAX_MULTIPV = 10

# SVG board size in pixels.
BOARD_SIZE = 540

# Chess.com-like board colors.
BOARD_COLORS = {
    "square light": "#EEEED2",
    "square dark": "#769656",
}
