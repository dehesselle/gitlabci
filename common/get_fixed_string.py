def get_fixed_str(text: str, length: int) -> str:
    # Turn a string into a fixed-width string by either truncating or padding it.
    if len(text) > length:
        text = text[:length-1] + "…"
    return text.ljust(length)
