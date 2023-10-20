from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path, WindowsPath


class Settings(BaseSettings):
    DB_NAME: str
    DB_ECHO: bool
    BASE_DIR: WindowsPath = Path(__file__).parent.parent.parent

    BOT_TOKEN: str
    BOT_ID: int

    CRYSTALPAY_LOGIN: str
    CRYSTALPAY_SECRET: str
    CRYSTALPAY_SALT: str

    YOUTUBE_API_KEY: str

    ID_REPORT_GROUP: int
    ID_REPORT_ADMIN: int
    REPORT_API_ID: int
    REPORT_API_HASH: str

    BOT_PORT: int
    BOT_WEBHOOK_SECRET: str
    WEBHOOK_PATH: str
    BASE_WEBHOOK_URL: str

    ID_AUTOSEO_ADMIN: int
    AUTOSEO_API_ID: int
    AUTOSEO_API_HASH: str

    @property
    def DATABASE_URL_SQLITE(self):
        return f"sqlite+aiosqlite:///{self.BASE_DIR}/{self.DB_NAME}.sqlite3"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}\.env")


settings = Settings()
