"""Streamlit UI styling helpers."""

from __future__ import annotations

import streamlit as st


def inject_custom_css() -> None:
    """Inject the custom CSS used by the Streamlit interface.

    The CSS avoids wrapping Streamlit widgets in custom HTML containers because
    Streamlit does not reliably preserve that structure across separate calls.
    """

    st.markdown(
        """
        <style>

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(118,150,86,0.16), transparent 30%),
                    linear-gradient(135deg, #0f1117 0%, #151821 48%, #101218 100%);
            }

            .block-container {
                padding: 2.4rem 3rem 2rem 3rem;
                max-width: 1500px;
            }

            section[data-testid="stSidebar"] {
                background: #171a23;
                border-right: 1px solid rgba(255,255,255,0.08);
            }

            .app-title {
                text-align: center;
                font-size: 2.45rem;
                font-weight: 900;
                letter-spacing: -0.04em;
                color: #f8fafc;
                margin-bottom: 2.2rem;
            }

            .section-title {
                height: 28px;
                display: flex;
                align-items: center;
                font-size: 1.05rem;
                font-weight: 850;
                color: #f8fafc;
                margin-bottom: 0.75rem;
            }

            .result-summary {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                background: rgba(255,255,255,0.055);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                margin-bottom: 1.1rem;
            }

            .result-block {
                display: flex;
                flex-direction: column;
                gap: 0.15rem;
            }

            .result-label {
                font-size: 0.72rem;
                color: #9ca3af;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 800;
            }

            .best-move {
                font-size: 1.85rem;
                font-weight: 900;
                color: #86efac;
                line-height: 1;
            }

            .result-value {
                font-size: 1.25rem;
                font-weight: 850;
                color: #f8fafc;
                line-height: 1;
            }

            .board-label {
                font-size: 0.95rem;
                font-weight: 850;
                color: #e5e7eb;
                margin-bottom: 0.55rem;
            }

            .helper-text {
                color: #9ca3af;
                font-size: 0.85rem;
                margin-top: 0.75rem;
            }

            textarea {
                font-size: 0.9rem !important;
                border-radius: 14px !important;
            }

            div[data-testid="stForm"] {
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 20px;
                padding: 1rem;
                background: rgba(255,255,255,0.04);
            }

            .stButton > button {
                border-radius: 14px;
                height: 3rem;
                font-weight: 850;
                border: none;
                background: linear-gradient(135deg, #769656, #4f7d3a);
                color: white;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, #86a965, #5c8d45);
                color: white;
                border: none;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 16px;
                overflow: hidden;
            }

            h1, h2, h3, h4 {
                color: #f8fafc;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
