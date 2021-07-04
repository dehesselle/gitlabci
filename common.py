import sty   # pip install sty


def to_fixed_len(text: str, length: int) -> str:
    """Truncate or pad a string to a specified length."""
    if len(text) > length:
        text = text[:length-1] + "…"
    return text.ljust(length)


def get_status_color(status: str) -> str:
    # Set a color depending on status.
    if status == "pending":
        return sty.fg(214)  # orange
    elif status == "created":
        return sty.fg.rs
    elif status == "running":
        return sty.fg(226)  # yellow
    elif status == "success":
        return sty.fg.green
    elif status == "canceled":
        return sty.fg(124)  # dark red
    elif status == "skipped":
        return sty.fg.li_black
    elif status == "failed":
        return sty.fg(196)  # light red
    else:
        return sty.fg.rs
