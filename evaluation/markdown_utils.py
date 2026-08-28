def escape_markdown(text: str) -> str:

    if text is None:
        return ""

    return (
        str(text)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("#", "\\#")
        .replace("*", "\\*")
        .replace("_", "\\_")
        .replace("`", "\\`")
    )