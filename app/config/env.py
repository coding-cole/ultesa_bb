from pydantic import BaseSettings


class Settings(BaseSettings):
    cluster_user_password: str
    cluster_user_name: str
    cluster_name: str
    mongo_link: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    password_token_expire_minutes: int
    firebase_email: str
    firebase_password: str

    class Config:
        env_file = ".env"


settings = Settings()


