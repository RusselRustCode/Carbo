from pydantic_settings import BaseSettings, SettingsConfigDict

class DataPipelineSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "admin_carbon"
    MINIO_SECRET_KEY: str = "supersecretpassword"
    MINIO_BUCKET: str = "carbon-datalake"
    MINIO_SECURE: bool = False

data_settings = DataPipelineSettings()
