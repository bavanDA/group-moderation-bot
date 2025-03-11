from pathlib import Path
import yaml


class LocaleKeys:
    # User-facing messages
    welcome = "welcome"
    unauthorized = "unauthorized"
    prompt_add_word = "prompt_add_word"
    prompt_remove_word = "prompt_remove_word"
    filtered_words_list = "filtered_words_list"

    # Commands
    add_words = "add_words"
    remove_words = "remove_words"
    show_words = "show_words"
    unknown_option = "unknown_option"

    # Responses
    word_added = "word_added"
    word_exists = "word_exists"
    word_removed = "word_removed"
    word_not_found = "word_not_found"
    empty_word_list = "empty_word_list"

    lang_changed = "lang_changed"

    warning = "warning"
    warning_msg = "warning_msg"
    h3_mute = "3h_mute"
    permanent_mute = "permanent_mute"
    mute_msg = "mute_msg"
    mute_reason = "mute_reason"


class LocaleManager:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = self.load_locale(lang)

    def load_locale(self, lang: str) -> dict:
        base_path = Path(__file__).resolve(
        ).parent.parent
        locale_path = base_path / "locales" / f"{lang}.yml"

        if locale_path.exists():
            with locale_path.open("r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        return {}

    def get(self, key: str) -> str:
        key_value = getattr(LocaleKeys, key, None)
        print(key_value)
        if key_value:
            return self.translations.get(key_value, f"[{key_value} not found]")
        return f"[{key} not found]"

    def set_language(self, lang: str) -> None:
        self.lang = lang
        self.translations = self.load_locale(lang)
