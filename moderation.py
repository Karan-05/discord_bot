"""
moderation.py – tiny helper around the OpenAI moderation endpoint
Adds verbose debug logging of the raw response for troubleshooting.
"""

from __future__ import annotations
import os
import logging
import openai

# ---------- logging setup ----------
logger = logging.getLogger(__name__)
# (bot.py sets the root config – here we just grab the child logger)
# ------------------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "text-moderation-latest"        # replace if model name changes


def is_toxic(content: str) -> tuple[bool, str]:
    """
    Returns (flagged_bool, top_category_str).
    Logs the full OpenAI response for visibility.
    """
    if not openai.api_key:
        logger.error("OPENAI_API_KEY missing! Can't call moderation endpoint.")
        return False, ""

    try:
        response = openai.moderations.create(input=content, model=MODEL_NAME)
    except Exception as exc:
        logger.exception("OpenAI moderation call failed: %s", exc)
        return False, ""

    # --- debug dump ----------------------------------------------------------
    logger.debug("OpenAI raw moderation response: %s", response)
    # ------------------------------------------------------------------------

    res = response.results[0]
    if not res.flagged:
        return False, ""

    # pick a representative category for logging / UX
    categories = res.categories
    top_cat = (
        "hate"          if categories.hate          else
        "harassment"    if categories.harassment    else
        "self-harm"     if categories.self_harm     else
        "sexual"        if categories.sexual        else
        "violence"      if categories.violence      else
        "unsafe"
    )
    return True, top_cat
