from pathlib import Path
import json

from settings import *
from helpers import *
from genWeb import *
from genKotlin import *
from genWeb import *


Path(OUT_KOTLIN_DIR).mkdir(exist_ok=True, parents=True)
Path(OUT_WEB_DIR).mkdir(exist_ok=True, parents=True)


def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for theme in data["themes"]:
        name = theme["name"]

        # определяем группу и цвет для структуры папок
        group_name_folder = name.lower()

        # название группы для вебки удобнее будет использовать camel case поэтому добавим еще и такую переменную
        group_name_folder_camel = to_camel(group_name_folder)

        # папки для web/css и web/ts
        web_css_dir = Path(OUT_WEB_DIR) / group_name_folder_camel / OUT_CSS_DIR
        web_ts_dir = Path(OUT_WEB_DIR) / group_name_folder_camel

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

        # Color.kt
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
        ts_filename = "index.ts"
        with open(web_ts_dir / ts_filename, "w", encoding="utf-8") as f:
            f.write(ts_code)

    print("Генерация завершена ✓")


if __name__ == "__main__":
    main()
