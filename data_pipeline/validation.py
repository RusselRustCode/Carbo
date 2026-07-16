import pandas as pd
from data_pipeline.s3_client import S3Storage

def validate_silver(silver_key: str) -> None:
    storage = S3Storage()
    buffer = storage.download_to_buffer(silver_key)


    df = pd.read_parquet(buffer)
    print("=" * 60)
    print(f"Файл: {silver_key}")
    print(f"Строк: {len(df)}, Колонок: {len(df.columns)}")
    print("=" * 60)

    print("\n🔍 Схема:")
    print(df.dtypes.to_string())

    print("\n👀 Первые 5 колонок")
    print(df.head().to_string())

    print("\n📊 Null кол-во:")
    print(df.isnull().sum().to_string())

    # Сравнение размеров
    import sys
    buffer.seek(0, 2)
    parquet_size = buffer.tell()
    print(f"\n💾 Parquet размер: {parquet_size / 1024:.1f} KB")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.validation <silver_key>")
        sys.exit(1)

    validate_silver(sys.argv[1])