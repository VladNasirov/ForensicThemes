# --------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# --------------------------------------------------------------
def to_camel(name: str):
    return "".join(part.capitalize() for part in name.replace("-", " ").split())


def normalize_key(k: str) -> str:
    return "--md-sys-color-" + k.replace("_", "-")


def palette_suffix(palette_name: str) -> str:
    if palette_name == "hc":
        return "-high-contrast"
    if palette_name == "mc":
        return "-mid-contrast"
    return ""


def sync_palette_group(group: dict):
    main = group.get("main", {})
    hc = group.get("hc", {})
    mc = group.get("mc", {})

    for key, value in main.items():
        if key not in hc:
            hc[key] = value
        if key not in mc:
            mc[key] = value

    group["hc"] = hc
    group["mc"] = mc
    return group


def snake_case_to_camel(snake_string):
    """
    Converts a string from snake-case to lower camelCase.

    Args:
        kebab_string (str): The input string in kebab-case.

    Returns:
        str: The converted string in lower camelCase.
    """
    words = snake_string.split('-')
    camel_case_words = [words[0]] + [word.capitalize() for word in words[1:]]
    return "".join(camel_case_words)
