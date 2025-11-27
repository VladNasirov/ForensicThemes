import json
import os
from pathlib import Path

# ========= НАСТРОЙКИ =========
DEPTARTMENT_NAME = "Forensic"
INPUT_JSON = "../themes.json"
OUT_KOTLIN_DIR = "out_kotlin"
OUT_WEB_DIR = "web"
OUT_TS_DIR = "ts"
OUT_CSS_DIR = "css"
PACKAGE_NAME = "com.example.compose"
# =============================

Path(OUT_KOTLIN_DIR).mkdir(exist_ok=True, parents=True)
Path(OUT_WEB_DIR).mkdir(exist_ok=True, parents=True)


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


# --------------------------------------------------------------
# ГЕНЕРАЦИЯ KOTLIN
# --------------------------------------------------------------
def gen_kotlin_colors(theme_name: str, palettes: dict) -> str:
    kt_name = to_camel(theme_name)
    lines = [f"package {PACKAGE_NAME}", "", "import androidx.compose.ui.graphics.Color", ""]

    for mode, groups in palettes.items():
        for palette_name, palette in groups.items():
            suffix = ""
            if palette_name == "hc":
                suffix = "HighContrast"
            elif palette_name == "mc":
                suffix = "MediumContrast"
            for k, v in palette.items():
                color_name = f"{k}{mode.capitalize()}{suffix}"
                lines.append(f"val {color_name} = Color({v})")  # v должен быть 0xFFRRGGBB
    return "\n".join(lines)

def gen_kotlin_theme_full(theme_name: str, palettes: dict) -> str:
    kt_name = to_camel(theme_name)
    lines = [f"package {PACKAGE_NAME}",
             "import android.app.Activity",
             "import android.os.Build",
             "import androidx.compose.foundation.isSystemInDarkTheme",
             "import androidx.compose.material3.MaterialTheme",
             "import androidx.compose.material3.lightColorScheme",
             "import androidx.compose.material3.darkColorScheme",
             "import androidx.compose.material3.dynamicDarkColorScheme",
             "import androidx.compose.material3.dynamicLightColorScheme",
             "import androidx.compose.material3.Typography",
             "import androidx.compose.runtime.Composable",
             "import androidx.compose.runtime.Immutable",
             "import androidx.compose.ui.graphics.Color",
             "import androidx.compose.ui.graphics.toArgb",
             "import androidx.compose.ui.platform.LocalContext",
             ""]


    # ---------------- ColorSchemes ----------------
    for mode, groups in palettes.items():
        for palette_name, palette in groups.items():
            scheme_name = mode
            if palette_name == "mc":
                scheme_name += "MediumContrast"
            elif palette_name == "hc":
                scheme_name += "HighContrast"
            scheme_name = scheme_name + "Scheme"
            func = "lightColorScheme" if mode == "light" else "darkColorScheme"
            lines.append(f"private val {scheme_name} = {func}(")
            for key, _ in palette.items():
                color_var_name = f"{key}{mode.capitalize()}"
                if palette_name == "mc":
                    color_var_name += "MediumContrast"
                elif palette_name == "hc":
                    color_var_name += "HighContrast"
                lines.append(f"    {key} = {color_var_name},")
            lines.append(")\n")

    # ---------------- ColorFamily ----------------
    lines += [
        "@Immutable",
        "data class ColorFamily(",
        "    val color: Color,",
        "    val onColor: Color,",
        "    val colorContainer: Color,",
        "    val onColorContainer: Color",
        ")",
        "",
        "val unspecified_scheme = ColorFamily(",
        "    Color.Unspecified, Color.Unspecified, Color.Unspecified, Color.Unspecified",
        ")",
        ""
    ]

    # ---------------- AppTheme ----------------
    lines += [
        "@Composable",
        "fun AppTheme(",
        "    darkTheme: Boolean = isSystemInDarkTheme(),",
        "    dynamicColor: Boolean = true,",
        "    content: @Composable () -> Unit",
        ") {",
        "    val colorScheme = when {",
        "        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {",
        "            val context = LocalContext.current",
        "            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)",
        "        }",
        "        darkTheme -> darkScheme",
        "        else -> lightScheme",
        "    }",
        "",
        "    MaterialTheme(",
        "        colorScheme = colorScheme,",
        "        typography = AppTypography,",
        "        content = content",
        "    )",
        "}"
    ]

    return "\n".join(lines)

    
def gen_kotlin_type() -> str:
    lines = [
        f"package {PACKAGE_NAME}",
        "",
        "import androidx.compose.material3.Typography",
        "import androidx.compose.ui.text.TextStyle",
        "import androidx.compose.ui.text.font.FontFamily",
        "import androidx.compose.ui.text.font.FontWeight",
        "import androidx.compose.ui.unit.sp",
        "",
        "val AppTypography = Typography()"
    ]
    return "\n".join(lines)
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


# --------------------------------------------------------------
# ОСНОВНОЙ КОД
# --------------------------------------------------------------
def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for theme in data["themes"]:
        name = theme["name"]

        # определяем группу и цвет для структуры папок
        group_name_folder = name.lower()

        # папки для web/css и web/ts
        web_css_dir = Path(OUT_WEB_DIR) / "css" / group_name_folder
        web_ts_dir = Path(OUT_WEB_DIR) / "ts" / group_name_folder

        # папка для Kotlin остается отдельно
        kt_out_dir = Path(OUT_KOTLIN_DIR) / group_name_folder
        kt_out_dir.mkdir(parents=True, exist_ok=True)

        web_css_dir.mkdir(parents=True, exist_ok=True)
        web_ts_dir.mkdir(parents=True, exist_ok=True)

        palettes = {}
        if "lightPalette" in theme:
            palettes["light"] = sync_palette_group(theme["lightPalette"])
        if "darkPalette" in theme:
            palettes["dark"] = sync_palette_group(theme["darkPalette"])

        # Kotlin
        kt_out_dir = Path(OUT_KOTLIN_DIR) / group_name_folder
        kt_out_dir.mkdir(parents=True, exist_ok=True)
        
        #Color.kt
        kt_colors_code = gen_kotlin_colors(name, palettes)
        with open(kt_out_dir / "Color.kt", "w", encoding="utf-8") as f:
            f.write(kt_colors_code)

        # Theme.kt
       # Theme.kt
        kt_theme_code = gen_kotlin_theme_full(name, palettes)
        with open(kt_out_dir / "Theme.kt", "w", encoding="utf-8") as f:
            f.write(kt_theme_code)

        # Type.kt
        kt_type_code = gen_kotlin_type()
        with open(kt_out_dir / "Type.kt", "w", encoding="utf-8") as f:
            f.write(kt_type_code)

        # CSS
        css_files = gen_css_files(palettes)
        for fname, code in css_files.items():
            with open(web_css_dir / fname, "w", encoding="utf-8") as f:
                f.write(code)

        # TypeScript
        ts_code = gen_ts_interface(name, palettes)
        ts_filename = f"{to_camel(name)}.ts"
        with open(web_ts_dir / ts_filename, "w", encoding="utf-8") as f:
            f.write(ts_code)

    print("Генерация завершена ✓")


if __name__ == "__main__":
    main()
