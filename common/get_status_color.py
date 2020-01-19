from sty import fg   # pip install sty


def get_status_color(status: str) -> str:
    # Set a color depending on status.
    if status == "pending":
        return fg(214)  # orange
    elif status == "created":
        return fg.rs
    elif status == "running":
        return fg(226)  # yellow
    elif status == "success":
        return fg.green
    elif status == "canceled":
        return fg(124)  # dark red
    elif status == "skipped":
        return fg.li_black
    elif status == "failed":
        return fg(196)  # light red
    else:
        return fg.rs
