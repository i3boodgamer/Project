from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict




class DatabaseConfig(BaseModel):
    NAME: str
    USER: str
    PASS: str
    HOST: str
    PORT: str
    
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    
    
    
    convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    
    @property
    def get_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
    


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./file.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    
    db: DatabaseConfig


settings = Settings()