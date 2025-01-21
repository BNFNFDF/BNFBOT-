import os
from importlib import import_module
from typing import Any, ClassVar


class Config:
    AS_DOCUMENT = False
    AUTHORIZED_CHATS = ""
    BASE_URL = ""
    BASE_URL_PORT = 80
    BOT_TOKEN = ""
    CMD_SUFFIX = ""
    DATABASE_URL = ""
    DEFAULT_UPLOAD = "rc"
    DOWNLOAD_DIR = "/usr/src/app/downloads/"
    EXTENSION_FILTER = ""
    FFMPEG_CMDS: ClassVar[dict[str, list[str]]] = {}
    FILELION_API = ""
    GDRIVE_ID = ""
    INCOMPLETE_TASK_NOTIFIER = False
    INDEX_URL = ""
    IS_TEAM_DRIVE = False
    LEECH_DUMP_CHAT = ""
    LEECH_FILENAME_PREFIX = ""
    LEECH_SPLIT_SIZE = 2097152000
    MEDIA_GROUP = False
    MIXED_LEECH = False
    MEGA_EMAIL = ""
    MEGA_PASSWORD = ""
    NAME_SUBSTITUTE = ""
    OWNER_ID = 0
    QUEUE_ALL = 0
    QUEUE_DOWNLOAD = 0
    QUEUE_UPLOAD = 0
    RCLONE_FLAGS = ""
    RCLONE_PATH = ""
    RCLONE_SERVE_URL = ""
    RCLONE_SERVE_USER = ""
    RCLONE_SERVE_PASS = ""
    RCLONE_SERVE_PORT = 8080
    RSS_CHAT = ""
    RSS_DELAY = 600
    RSS_SIZE_LIMIT = 0
    SEARCH_API_LINK = ""
    SEARCH_LIMIT = 0
    SEARCH_PLUGINS: ClassVar[list[str]] = []
    STOP_DUPLICATE = False
    STREAMWISH_API = ""
    SUDO_USERS = ""
    TELEGRAM_API = 0
    TELEGRAM_HASH = ""
    THUMBNAIL_LAYOUT = ""
    TORRENT_TIMEOUT = 0
    USER_TRANSMISSION = False
    UPSTREAM_REPO = ""
    UPSTREAM_BRANCH = "main"
    USER_SESSION_STRING = ""
    USE_SERVICE_ACCOUNTS = False
    WEB_PINCODE = False
    YT_DLP_OPTIONS = ""

    # INKYPINKY
    METADATA_KEY = ""
    WATERMARK_KEY = ""
    SET_COMMANDS = True
    TOKEN_TIMEOUT = 0
    PAID_CHANNEL_ID = 0
    PAID_CHANNEL_LINK = ""
    DELETE_LINKS = False
    FSUB_IDS = ""
    LOG_CHAT_ID = 0
    LEECH_FILENAME_CAPTION = ""

    @classmethod
    def get(cls, key):
        if hasattr(cls, key):
            return getattr(cls, key)
        raise KeyError(f"{key} is not a valid configuration key.")

    @classmethod
    def set(cls, key, value):
        if hasattr(cls, key):
            setattr(cls, key, value)
        else:
            raise KeyError(f"{key} is not a valid configuration key.")

    @classmethod
    def get_all(cls):
        return {
            key: getattr(cls, key)
            for key in cls.__dict__
            if not key.startswith("__") and not callable(getattr(cls, key))
        }

    @classmethod
    def load(cls):
        try:
            settings = import_module("config")
        except ModuleNotFoundError:
            return
        else:
            for attr in dir(settings):
                if hasattr(cls, attr):
                    value = getattr(settings, attr)
                    if not value:
                        continue
                    if isinstance(value, str):
                        value = value.strip()
                    if attr == "DEFAULT_UPLOAD" and value != "gd":
                        value = "rc"
                    elif (
                        attr
                        in [
                            "BASE_URL",
                            "RCLONE_SERVE_URL",
                            "INDEX_URL",
                            "SEARCH_API_LINK",
                        ]
                        and value
                    ):
                        value = value.strip("/")
                    setattr(cls, attr, value)

    @classmethod
    def load_dict(cls, config_dict):
        for key, value in config_dict.items():
            if hasattr(cls, key):
                if key == "DEFAULT_UPLOAD" and value != "gd":
                    value = "rc"
                elif (
                    key
                    in [
                        "BASE_URL",
                        "RCLONE_SERVE_URL",
                        "INDEX_URL",
                        "SEARCH_API_LINK",
                    ]
                    and value
                ):
                    value = value.strip("/")
                setattr(cls, key, value)


class SystemEnv:
    @classmethod
    def load(cls):
        config_vars = Config.get_all()
        for key in config_vars:
            env_value = os.getenv(key)
            if env_value is not None:
                converted_value = cls._convert_type(key, env_value)
                Config.set(key, converted_value)

    @classmethod
    def _convert_type(cls, key: str, value: str) -> Any:
        original_value = getattr(Config, key, None)
        if original_value is None:
            return value
        if isinstance(original_value, bool):
            return value.lower() in ("true", "1", "yes")
        if isinstance(original_value, int):
            try:
                return int(value)
            except ValueError:
                return original_value
        if isinstance(original_value, float):
            try:
                return float(value)
            except ValueError:
                return original_value
        return value
