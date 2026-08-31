import re


def sanitize_attribute(name: str) -> str:
    name = name.strip()

    name = re.sub(r"\s+", "_", name)

    name = re.sub(
        r"[^A-Za-z0-9_.-]",
        "",
        name,
    )

    return name