"""Streamlit entry point for the Stockfish PGN Analyzer."""

from __future__ import annotations

import streamlit as st

from src.board import (
    build_candidates_table,
    get_board_orientation,
    make_board_after_svg,
    make_board_before_svg,
)
from src.config import (
    DEFAULT_DEPTH,
    DEFAULT_MULTIPV,
    MAX_DEPTH,
    MAX_MULTIPV,
    MIN_DEPTH,
    MIN_MULTIPV,
)
from src.engine import analyze_position, format_score
from src.pgn import build_board_from_game, read_game_from_pgn
from src.ui import inject_custom_css


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Stockfish PGN Analyzer",
    page_icon="♟️",
    layout="wide",
)

# Apply the custom visual theme.
inject_custom_css()


# ============================================================
# APPLICATION HEADER
# ============================================================

st.markdown(
    '<div class="app-title">♟️ Stockfish PGN Analyzer</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:
    st.header("⚙️ Settings")

    # Stockfish depth controls how far the engine searches.
    # Higher values are stronger but slower.
    depth = st.slider(
        "Analysis depth",
        min_value=MIN_DEPTH,
        max_value=MAX_DEPTH,
        value=DEFAULT_DEPTH,
        step=1,
        help="Higher depth gives stronger analysis but takes longer.",
    )

    # MultiPV controls how many candidate moves Stockfish returns.
    multipv = st.slider(
        "Candidate moves",
        min_value=MIN_MULTIPV,
        max_value=MAX_MULTIPV,
        value=DEFAULT_MULTIPV,
        step=1,
        help="Number of candidate moves returned by Stockfish.",
    )


# ============================================================
# MAIN LAYOUT
# ============================================================

left_col, right_col = st.columns([0.9, 2.1], gap="large")


# ============================================================
# LEFT COLUMN: PGN INPUT
# ============================================================

with left_col:
    st.markdown('<div class="section-title">Paste PGN</div>', unsafe_allow_html=True)

    # A Streamlit form prevents the app from rerunning on every keystroke.
    # The analysis only starts when the user clicks the submit button.
    with st.form("analysis_form"):
        pgn_text = st.text_area(
            "Chess.com PGN",
            label_visibility="collapsed",
            height=330,
            placeholder="""[Event "Let's Play!"]
[Site "Chess.com"]
[Date "2026-06-19"]
[White "PlayerWhite"]
[Black "PlayerBlack"]
[Result "*"]

1. d4 d5 2. c4 e6 3. e3 *""",
        )

        submitted = st.form_submit_button(
            "Analyze position",
            type="primary",
            use_container_width=True,
        )

    st.markdown(
        '<div class="helper-text">Paste the PGN exactly as exported, including metadata.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RIGHT COLUMN: ANALYSIS OUTPUT
# ============================================================

with right_col:
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    # Keep the output area visually clean until the first form submission.
    if submitted:
        try:
            if not pgn_text.strip():
                st.warning("Please paste a PGN before running the analysis.")
                st.stop()

            # The spinner covers the complete parsing + engine analysis flow.
            with st.spinner("Stockfish is analyzing the position..."):
                # 1. Parse the PGN text.
                game = read_game_from_pgn(pgn_text)

                # 2. Rebuild the current board from the PGN mainline.
                board = build_board_from_game(game)

                # 3. Choose the board orientation.
                orientation = get_board_orientation(board)

                # 4. Ask Stockfish for the requested number of candidate moves.
                infos = analyze_position(
                    board=board,
                    depth=depth,
                    multipv=multipv,
                )

            # Stockfish returns candidate lines ordered from best to worst.
            best_info = infos[0]
            best_move = best_info["pv"][0]
            best_move_san = board.san(best_move)
            best_score = format_score(best_info["score"])

            # Main summary: best move, evaluation, and depth used.
            st.markdown(
                f"""
                <div class="result-summary">
                    <div class="result-block">
                        <div class="result-label">Best move</div>
                        <div class="best-move">{best_move_san}</div>
                    </div>
                    <div class="result-block">
                        <div class="result-label">Evaluation</div>
                        <div class="result-value">{best_score}</div>
                    </div>
                    <div class="result-block">
                        <div class="result-label">Depth</div>
                        <div class="result-value">{depth}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Before / after board comparison.
            before_col, after_col = st.columns(2, gap="large")

            with before_col:
                st.markdown('<div class="board-label">Before</div>', unsafe_allow_html=True)
                st.image(
                    make_board_before_svg(board, best_move, orientation),
                    use_container_width=True,
                )

            with after_col:
                st.markdown('<div class="board-label">After</div>', unsafe_allow_html=True)
                st.image(
                    make_board_after_svg(board, best_move, orientation),
                    use_container_width=True,
                )

            # Candidate moves table.
            # st.table automatically adapts to the number of rows selected by
            # the MultiPV slider, avoiding unnecessary empty space.
            st.markdown('<div class="section-title">Candidate moves</div>', unsafe_allow_html=True)
            st.table(build_candidates_table(board, infos))

        except Exception as error:
            st.error(f"Error: {error}")
