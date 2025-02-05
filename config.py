from pydantic import BaseModel

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class ApiPrefix (BaseModel):
    prefix: str = "/api"
    user_prefix: str = "/user"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONF__"
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    
    
settings: Settings = Settings()