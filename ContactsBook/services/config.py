from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    admin_email: str

    POSTGRESQL_URL: str
    SQLITE_URL: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379

    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
