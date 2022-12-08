from is_safe_url import is_safe_url as is_safe_url_

from flask import current_app


def is_safe_url(url: str) -> bool:
    return is_safe_url_(url, current_app.config["SAFE_DOMAINS"])
