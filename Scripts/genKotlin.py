from settings import *
from helpers import *

# --------------------------------------------------------------
# ГЕНЕРАЦИЯ KOTLIN
# --------------------------------------------------------------


def gen_kotlin_colors(theme_name: str, palettes: dict) -> str:
    kt_name = to_camel(theme_name)
    lines = [f"package {PACKAGE_NAME}", "",
             "import androidx.compose.ui.graphics.Color", ""]

    for mode, groups in palettes.items():
        for palette_name, palette in groups.items():
            suffix = ""
            if palette_name == "hc":
                suffix = "HighContrast"
            elif palette_name == "mc":
                suffix = "MediumContrast"
            for k, v in palette.items():
                color_name = f"{k}{mode.capitalize()}{suffix}"
                # v должен быть 0xFFRRGGBB
                lines.append(f"val {color_name} = Color({v})")
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
