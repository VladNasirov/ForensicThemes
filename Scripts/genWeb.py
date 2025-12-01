from helpers import *

# --------------------------------------------------------------
# ГЕНЕРАЦИЯ CSS
# --------------------------------------------------------------


def gen_css_files(palettes: dict):
    outputs = {}
    for mode, groups in palettes.items():
        for palette_name, palette in groups.items():
            suffix = palette_suffix(palette_name)
            fname = f"{mode}{suffix}.css"
            selector = f".{mode}{suffix}"
            lines = [f"{selector} {{"]

            for k, v in palette.items():
                lines.append(f"  {normalize_key(k)}: {v};")

            lines.append("}")
            outputs[fname] = "\n".join(lines)
    return outputs


# --------------------------------------------------------------
# ГЕНЕРАЦИЯ TypeScript интерфейсов
# --------------------------------------------------------------

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


def gen_ts_interface(theme_name: str, palettes: dict) -> str:
    """
    Генерирует TS интерфейс с ключами всех цветов, в camelCase,
    без групп и без режимов. Все ключи объединяются из всех тем и палитр.
    """
    ts_name = to_camel(theme_name)

    # Собираем все ключи из всех режимов и палитр
    all_keys = set()
    for _, groups in palettes.items():
        for _, palette in groups.items():
            for k in palette.keys():
                all_keys.add(k)

    # Преобразуем в camelCase и отсортируем
    camel_keys = sorted(snake_case_to_camel(k) for k in all_keys)

    lines = [f"export default interface I{ts_name}Colors {{"]
    for key in camel_keys:
        lines.append(f"  {key}: string;")
    lines.append("}")

    return "\n".join(lines)
