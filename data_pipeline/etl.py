import pandas as pd
from io import BytesIO
from data_pipeline.s3_client import S3Storage

def clean_soil_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.dropna(how="all")

    if "sample_date" in df.columns:
        df["sample_date"] = pd.to_datetime(df["sample_date"], errors="coerce")

    numeric_cols = ["ph_level", "carbon_content_(%)", "nitrogen_(mg/kg)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def process_bronze_to_silver(bronze_key: str, task_id: str) -> str:
    """
    Читает CSV из Bronze, очищает и сохраняет как Parquet в Silver.

    Args:
        bronze_key: Object key файла в слое Bronze
        task_id: UUID задачи для формирования пути в Silver

    Returns:
        object_key созданного Parquet-файла в слое Silver
    """
    storage = S3Storage()

    buffer = storage.download_to_buffer(bronze_key)

    df = pd.read_csv(buffer)
    print(f"Сырые строки: {len(df)}")

    df_clean = clean_soil_data(df)
    print(f"Обработанные строки: {len(df_clean)} (удалено {len(df) - len(df_clean)})")

    parquet_buffer = BytesIO()
    df_clean.to_parquet(parquet_buffer, index=False, engine="pyarrow")
    parquet_buffer.seek(0)

    silver_key = f"silver/tables/lab_soil/task_{task_id}.parquet"
    storage.upload_bytes(parquet_buffer.getvalue(), silver_key)

    return silver_key

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m data_pipeline.etl <bronze_key> <task_id>")
        sys.exit(1)

    bronze_key = sys.argv[1]
    task_id = sys.argv[2]

    silver_key = process_bronze_to_silver(bronze_key, task_id)
    print(f"\nSilver ETL complete: {silver_key}")