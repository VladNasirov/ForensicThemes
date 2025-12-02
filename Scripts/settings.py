from pathlib import Path
# ========= НАСТРОЙКИ =========
# General
DEPTARTMENT_NAME = "Forensic"
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_JSON = PROJECT_ROOT / "themes.json"

# Web
OUT_WEB_DIR = PROJECT_ROOT / "WEB"
OUT_TS_DIR = "ts"
OUT_CSS_DIR = "css"
OUT_TS_CONFIG_FILENAME = "config.ts"

# Kotlin
OUT_KOTLIN_DIR = "Kotlin"
PACKAGE_NAME = "com.example.compose"
# =============================
