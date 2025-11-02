import re
from typing import Any, Dict, Optional
from datetime import datetime

import dateparser
from dateparser.search import search_dates


def extract_task_and_time(text: str) -> Dict[str, Any]:
    """
    Extract a task description and a datetime from `text`.

    Returns a dict with keys:
      - "task": cleaned task string (lowercased)
      - "time": a `datetime.datetime` object parsed from the text, or `None` if not found

    The function uses `dateparser.search.search_dates` to locate date/time phrases
    and removes those phrases (plus common reminder words) from the returned task.
    """

    if not text or not text.strip():
        return {"task": "", "time": None}

    # Find date/time expressions in the text (case-insensitive)
    # Prefer future dates for relative expressions like 'tomorrow'
    results = search_dates(text, settings={"PREFER_DATES_FROM": "future"})
    time: Optional[datetime] = None
    matched_texts = []
    if results:
        # search_dates returns a list of (matched_text, datetime)
        matched_texts = [m[0] for m in results if m and m[0]]
        time = results[0][1]

    cleaned = text

    # Remove the matched date phrases (safe, case-insensitive)
    for mt in matched_texts:
        try:
            cleaned = re.sub(re.escape(mt), "", cleaned, flags=re.IGNORECASE)
        except re.error:
            # fallback: simple replace
            cleaned = cleaned.replace(mt, "")

    # Remove common reminder words/phrases while avoiding substring damage
    keyword_patterns = [r"\bremind me to\b", r"\bremind me\b", r"\bto\b",
                        r"\bat\b", r"\bin\b", r"\bon\b",
                        r"\btomorrow\b", r"\btoday\b"]
    for pat in keyword_patterns:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)

    # Collapse whitespace and strip surrounding punctuation
    cleaned = re.sub(r"[,:;\-]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.strip(" -:;,.!? \n\r\t")

    task = cleaned.lower()

    return {"task": task, "time": time}
